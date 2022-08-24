from dataclasses import dataclass, field, fields
from pathlib import Path
import re
from typing import IO, Iterator
import requests
import tarfile
import time
from datetime import datetime, date
from dateutil.parser import parse as parsedate
import concurrent.futures
from .models import x86_64, aarch64, lastModified, Archs, Branches


MIRROR = "https://mirrors.manjaro.org/repo"
CACHE_DIR = "/tmp"
MAX_WORKERS = 10


class Downloader():
    URL_TEMPLATE = "{MIRROR}/{prefix}{branch}/{repo}/{arch}/{repo}.db"

    def __init__(self, arch: Archs, branches, repos, files_times) -> None:
        self.items = []
        self.update = set()
        self.arch = arch
        self.branches = branches
        self.repos = repos
        self.files_times = files_times
        self.files_times.objects.filter(arch=arch.name)

    @staticmethod
    def filename(arch: str, branch: str, repo: str) -> Path:
        return Path(CACHE_DIR) / arch / branch / f"{repo}.db"

    def format_url(self, branch, repo) -> str:
        return self.URL_TEMPLATE.format(
            MIRROR=MIRROR,
            branch=branch,
            repo=repo,
            arch=self.arch.name,
            prefix="" #if self.arch == Archs.x86_64 else "arm-"
            )

    def run(self) -> set:
        """run threads for download"""
        self.update = set()
        futures = []
        with concurrent.futures.ThreadPoolExecutor(MAX_WORKERS) as executor:
            for branch in self.branches:
                filename = self.filename(self.arch.name, branch, "core")
                filename.parent.mkdir(parents=True, exist_ok=True)
                for repo in self.repos:
                    futures.append(executor.submit(
                        self.download,
                        self.format_url(branch, repo),
                        self.filename(self.arch.name, branch, repo),
                        self.arch.name, branch, repo,
                        self.files_times
                        ))
            for future in concurrent.futures.as_completed(futures):
                try:
                    ok, url, repo = future.result()
                    if ok:
                        self.update.add(repo)
                        print("Updating:", url)
                except Exception:
                    raise
        return self.update

    @staticmethod
    def download(url: str, local_filename: Path, arch, branch, repo, files_times) -> tuple:
        """download one file in thread"""
        response = requests.head(url=url, timeout=30)  
        if not response.ok:
            #TODO error use another mirror
            raise Exception("Download Error", url, response)

        try:
            remote_datetime = parsedate(response.headers['Last-Modified']).astimezone()
        except Exception as e:
            print(arch, branch, repo, e)
            remote_datetime = datetime.now().astimezone()
        local_datetime = remote_datetime

        try:
            model = files_times.objects.get(arch=arch, branch=branch, repo=repo)
            local_datetime = model.date
            model.status=response.status_code
            model.save()
        except files_times.DoesNotExist:
            files_times(
                arch=arch, branch=branch, repo=repo,
                date=local_datetime,
                status=response.status_code
            ).save()
            print(f"{arch:10} {branch:14} {repo:16} to download")
        
        if local_datetime == remote_datetime and local_filename.exists():
            print("Nothing to do", url, repo)
            return False, url, repo

        resp = requests.get(url=url, timeout=20)
        if resp.ok:
            with open(local_filename, 'wb') as fdb:
                fdb.write(resp.content)
            model = files_times.objects.get(arch=arch, branch=branch, repo=repo)
            model.date=remote_datetime
            model.status=response.status_code
            model.save()
            return True, url, repo
        return False, url, repo


@dataclass(slots=True)
class PackageVersions:
    stable: str = ""
    testing: str = ""
    unstable: str = ""

    def all_equal(self) -> bool:
        """new version"""
        return len(set(getattr(self, x.name) for x in fields(self))) == 1

    def one_empty(self) -> bool:
        """new package or deleted"""
        return "" in set(getattr(self, x.name) for x in fields(self))


@dataclass(slots=True)
class PackageAlpm:
    """ alpm desc file"""
    repo: str
    idx: int
    name: str = ""
    base: str = ""
    groups: str = ""    # base-devel
    # version: str = ""
    desc: str = ""
    csize: int = 0
    isize: int = 0
    # md5sum : str
    # sha256sum : str
    # pgpsig : str
    url: str = ""
    license: tuple[str] = field(default_factory=tuple)
    arch: str = "any"
    builddate: int = 0
    packager: str = ""
    replaces: tuple[str] | None = None      # = field(default_factory=tuple)
    conflicts: tuple[str] | None = None       # = field(default_factory=tuple)
    provides: tuple[str] | None = None       # = field(default_factory=tuple)
    depends: tuple[str] | None = None       # = field(default_factory=tuple)

    # versions by branches
    versions: PackageVersions = field(default_factory=PackageVersions, init=False)  # dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        # self.versions = PackageVersions()
        pass

    def inject(self, desc: str, branch: Branches) -> object:
        """set datas from alpm desc file"""
        excludes = ("optdepends",)
        for key, value in self.kv_from_str(desc):
            if key in excludes:
                continue
            if key == "version":
                try:
                    setattr(self.versions, branch.name, value)
                except AttributeError:
                    pass    # branch not exists ?
                continue
            try:
                setattr(self, key, value)
            except AttributeError:
                print("\n Key not found ????\n", key, ":", value)
                raise
        return self

    @property
    def key(self) -> str:
        """create unique key name-repo"""
        return f"{self.name}-{self.repo}"

    @property
    def builddate_str(self) -> str:
        """builddate to string"""
        # "Thu 19 May 2022 19:35:15 GMT"  - BAD format ?
        #return time.strftime("%a %d %b %Y %X %Z", time.gmtime(self.builddate))    # time.gmtime
        return time.strftime("%Y-%m-%d", time.gmtime(self.builddate))

    def version(self, branch: Branches) -> str:
        return getattr(self.versions, branch.name)

    def in_branch(self, branch: Branches):
        """package exists in this branch ?"""
        return bool(getattr(self.versions, branch.name))

    def is_updated(self) -> bool:
        """One version or more is different ?"""
        return not self.versions.all_equal()

    @staticmethod
    def kv_from_str(text: str) -> Iterator:
        """Yields key / value pairs from a string."""
        INT_KEYS = {
            '%BUILDDATE%',
            '%CSIZE%',
            '%ISIZE%'
            }
        LIST_KEYS = {
            '%DEPENDS%',
            '%MAKEDEPENDS%',
            '%REPLACES%',
            '%CONFLICTS%',
            '%OPTDEPENDS%',
            '%PROVIDES%', 
            '%LICENSE%',
            '%CHECKDEPENDS%'
            }

        LIST_SEP = '\n'
        ITEM_SEP = '\n\n'
        KEY_VALUE_SEP = '\n'
        for item in text.split(ITEM_SEP):
            if not item.strip():
                continue
            key, value = item.split(KEY_VALUE_SEP, maxsplit=1)

            if key in [
                '%FILENAME%',
                '%PGPSIG%',
                '%MD5SUM%',
                '%SHA256SUM%',
                '%CHECKDEPENDS%',
                '%MAKEDEPENDS%'
                ]:
                continue

            if value == 'None':
                continue

            if key in INT_KEYS:
                value = int(value)
            elif key in LIST_KEYS:
                value = tuple(value.split(LIST_SEP))
            yield key.replace('%', '').lower(), value

    @classmethod
    def kv_from_file(cls, fdesc: IO) -> Iterator:
        """Yields key / value pairs from a file."""
        content = fdesc.read().decode()
        yield from cls.kv_from_str(content)


class AlpmDb:
    MAX = 99550

    def __init__(self, arch: Archs, repos) -> None:
        self.arch = arch
        self.repos = repos
        self.pkgs: dict[str, PackageAlpm] = {}

    def parse_files(self):
        """parse files in all branches, all repos"""
        self.pkgs = {}
        for branch in Branches:
            if "aarch64" in self.arch.name:
                branch_name = "arm-" + branch.name
            else:
                branch_name = branch.name

            if not Downloader.filename(self.arch.name, branch_name, "repo").parent.exists():
                # this branch is not in setup
                print(" branch not found")
                continue
            for repo in self.repos:
                index = 0
                filename = Downloader.filename(self.arch.name, branch_name, repo)
                pkg : PackageAlpm
                with tarfile.open(filename, "r") as tar:
                    for tarinfo in tar:
                        if not (tarinfo.isfile() or tarinfo.name.endswith(".desc")):
                            continue
                        fdesc = tar.extractfile(tarinfo)
                        if not fdesc:
                            raise Exception(f"invalid desc ! {tarinfo}")
                        pkg = PackageAlpm(repo=repo, idx=len(self.pkgs)+1)
                        pkg.inject(fdesc.read().decode(), branch=branch)
                        key = pkg.key
                        if self.pkgs.get(key):
                            setattr(
                                self.pkgs[key].versions,
                                branch.name,
                                getattr(pkg.versions, branch.name)
                            )
                        else:
                            self.pkgs[pkg.key] = pkg
                        # pkg = dict(Package.kv_from_file(f))
                        index += 1
                        if index > AlpmDb.MAX:
                            break


def update_db(arch, repos, pkg_model, test=False):
    db = AlpmDb(arch, repos)
    db.parse_files()
    start = time.perf_counter()
    try:
        print(f"sql update {arch.name} :: for {len(db.pkgs)} packages in", db.repos)
        for repo in db.repos:
            # pkg_model.objects.filter(architecture=arch.value, repo=repo).delete()
            pkg_model.objects.filter(repo=repo).delete()
            print(f"sql update {arch.name} :: remove repo {repo}")
        pkg: PackageAlpm
        objs = []
        for _, pkg in db.pkgs.items():
            #print(pkg)
            try:
                objs.append(
                    pkg_model(
                        name=pkg.name,
                        repo=pkg.repo,
                        architecture=arch.value,  # not useful with proxyManagers
                        arch=pkg.arch,    # SELECT arch  from compare_packagemodel group by arch
                        stable=pkg.version(Branches.stable),
                        testing=pkg.version(Branches.testing),
                        unstable=pkg.version(Branches.unstable),
                        group=pkg.groups,
                        url=pkg.url,
                        packager=pkg.packager,
                        builddate=pkg.builddate_str,
                        last_modified=date.today().strftime("%B %d, %Y")
                        )
                    )
            except Exception as e:
                #print(pkg, pkg.packager, pkg.builddate_str, e)
                raise
        if not test:
            ret = len(pkg_model.objects.bulk_create(objs))
            print(f"sql update :: bulk_created: {int(ret)} packages")
        else:
            print("TEST: no DB update")
    finally:
        hours, rem = divmod(time.perf_counter() - start, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"sql update {arch} :: end {hours:.0f} {minutes:.0f}:{seconds:.0f}")
    #raise Exception("One test") #TODO for remove, was ok for test error log
    # TODO remove:    CACHE_DIR / arch

def send_log(err:Exception):
    from wagtail.core.models import Page
    from wagtail.core.log_actions import log
    try:
        page =Page.objects.get(title="Packages")
        log(
            instance=page, action='wagtail.workflow.cancel',
            #data={"error":"Exception xxxx"},    # wagtail page no display data ?
            title=f"[Update ERROR] {err}"
        )
    except: # wagtail.core.models.Page.DoesNotExist:
        pass


def update_x86_64(test_directory=None):
    arch = Archs.x86_64
    branches = ("stable", "testing", "unstable")
    repos = ("multilib", "core", "extra", "community", "kde-unstable")
    global CACHE_DIR
    if test_directory:
        CACHE_DIR = test_directory

    download = Downloader(arch, branches, repos, lastModified)
    if repos := download.run():
        try:
            update_db(arch, repos, x86_64, bool(test_directory))
        except Exception as err:
            lastModified.objects.filter(arch=arch.name).update(status=f"[ERROR] {err}")
            print("EXCEPTION !", err)
            send_log(err)


def update_aarch64(test_directory=None):
    arch = Archs.aarch64
    branches = ("arm-stable", "arm-testing", "arm-unstable")
    repos = ("core", "extra", "community", "kde-unstable", "mobile")
    global CACHE_DIR
    if test_directory:
        CACHE_DIR = test_directory

    download = Downloader(arch, branches, repos, lastModified)
    if repos := download.run():
        try:
            update_db(arch, repos, aarch64, bool(test_directory))
        except Exception as err:
            send_log(err)
