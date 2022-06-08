from dataclasses import dataclass, field, fields
import enum
from pathlib import Path
from typing import IO, Iterator
import requests
import tarfile
import time
import pytz
from datetime import datetime, date
#from datetime import date
from dateutil.parser import parse as parsedate
import concurrent.futures

MIRROR = "https://mirrors.manjaro.org/repo"
CACHE_DIR = "/tmp"


class Archs(enum.Enum):
    x86_64 = enum.auto()
    aarch64 = enum.auto()


class Branches(enum.Enum):
    stable = 0
    testing = 1
    unstable = 2


class Downloader():
    URL_TEMPLATE = "{MIRROR}/{prefix}{branch}/{repo}/{arch}/{repo}.db"

    def __init__(self, arch: Archs, branches, repos) -> None:
        self.items = []
        self.update = set()
        self.arch = arch
        self.branches = branches
        self.repos = repos

    @staticmethod
    def filename(arch: str, branch: str, repo: str) -> Path:
        return Path(CACHE_DIR) / arch / branch / f"{repo}.db"

    def format_url(self, branch, repo) -> str:
        return self.URL_TEMPLATE.format(
            MIRROR=MIRROR,
            branch=branch,
            repo=repo,
            arch=self.arch.name,
            prefix="" if self.arch == Archs.x86_64 else "arm-"
            )

    def run(self) -> set:
        """run threads for download"""
        self.update = set()
        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            for branch in self.branches:
                filename = self.filename(self.arch.name, branch, "core")
                filename.parent.mkdir(parents=True, exist_ok=True)
                for repo in self.repos:
                    futures.append(executor.submit(
                        self.download,
                        self.format_url(branch, repo),
                        self.filename(self.arch.name, branch, repo),
                        repo
                        ))
            for future in concurrent.futures.as_completed(futures):
                try:
                    ok, url, repo = future.result()
                    if ok:
                        self.update.add(repo)
                        print(ok, "for:", url)
                except Exception:
                    raise
        return self.update

    @staticmethod
    def download(url: str, local_filename: Path, repo) -> tuple:
        """download one file in thread"""
        response = requests.head(url=url, timeout=10)
        if not response.ok:
            raise Exception("Download Error", url, response)
        remote_datetime = parsedate(response.headers['Last-Modified']).astimezone()

        # Get local file's datetime
        # TODO replace with database table updates
        local_filename_datetime = datetime.fromtimestamp(local_filename.stat().st_mtime).astimezone() \
            if local_filename.exists() else None
        if local_filename_datetime and local_filename_datetime >= remote_datetime:
            return False, url, repo

        resp = requests.get(url=url, timeout=10)
        if resp.ok:
            with open(local_filename, 'wb') as fdb:
                fdb.write(resp.content)
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


    @property
    def packager_name(self) -> str:
        """packager without email"""
        try:
            return self.packager.split("<", 1)[0].strip()
        except IndexError:
            return self.packager

    @property
    def is_manjaro(self) -> bool:
        """package is make by manjaro ?"""
        return "manjaro.org" in self.packager

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
        INT_KEYS = {'%BUILDDATE%', '%CSIZE%', '%ISIZE%'}
        LIST_KEYS = {'%DEPENDS%', '%MAKEDEPENDS%', '%REPLACES%', '%CONFLICTS%',
                    '%OPTDEPENDS%', '%PROVIDES%', '%LICENSE%', '%CHECKDEPENDS%'}

        LIST_SEP = '\n'
        ITEM_SEP = '\n\n'
        KEY_VALUE_SEP = '\n'
        for item in text.split(ITEM_SEP):
            if not item.strip():
                continue
            key, value = item.split(KEY_VALUE_SEP, maxsplit=1)

            if key in ['%FILENAME%', '%PGPSIG%', '%MD5SUM%', '%SHA256SUM%',
                    '%CHECKDEPENDS%', '%MAKEDEPENDS%']:
                continue

            if value == 'None':
                continue

            if key in INT_KEYS:
                value = int(value)
            elif key in LIST_KEYS:
                value = tuple(value.split(LIST_SEP))
            yield key.replace('%', '').lower(), value
        #yield "versions", {"stable": "", "testing": "", "unstable": ""}

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
            if not Downloader.filename(self.arch.name, branch.name, "repo").parent.exists():
                # this branch is not in setup
                continue
            for repo in self.repos:
                i = 0
                filename = Downloader.filename(self.arch.name, branch.name, repo)
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
                        i += 1
                        if i > AlpmDb.MAX:
                            break
    
    def stats(self):    #TODO remove
        """some TEST"""
        for _, pkg in self.pkgs.items():
            # if not pkg.is_updated():
            #    continue
            if not pkg.versions.one_empty():
                continue
            print(repr(pkg))
            print(pkg.builddate_str)
            print(pkg.versions.stable)
            print(pkg.packager_name)
            for branch in Branches:
                print(f"is in {branch.name} ?", pkg.in_branch(branch), pkg.version(branch))
            print()


##################################

def check_last_update(url, arch, branch, repo, last_update_model):
    response = requests.head(url=url, timeout=10)
    if not response.ok:
        raise Exception("Download Error", url, response)

    remote_datetime = parsedate(response.headers['Last-Modified']).astimezone()

    try:
        model = last_update_model.objects.get(arch=arch, branch=branch, repo=repo)
        if model.last_update != remote_datetime:
            model.last_update = remote_datetime
            print(arch, branch, repo, "outdated, updating")
            return True
        else:
            print(arch, branch, repo, "no update needed")
            return False
    except last_update_model.DoesNotExist:
        last_update_model(arch=arch, branch=branch, repo=repo, last_update=remote_datetime).save()
        print(arch, branch, repo, "first time update")
        return True


def get_db(arch, branch, repo, last_update_model):
    mirror="https://mirror.easyname.at/manjaro"
    url = f"{mirror}/{branch}/{repo}/{arch}/{repo}.db"
    update = check_last_update(url, arch, branch, repo, last_update_model)
    if update:
        response = requests.get(url, stream=True)
        if response.ok:
            return response.raw
        else:
            print(url, response.status_code)
    else:
        return False


def parse_pkg_desc(fileobj, branch, repo, pkg_model, arch):
    it = iter(fileobj.readlines())
    name = ""
    try:
        while it:
            item = next(it).decode().strip()
            if "%NAME%" in item:
                name = next(it).decode().strip()
                try:
                    pkg_model.objects.get(name=name)
                except pkg_model.DoesNotExist:
                    update = date.today().strftime("%B %d, %Y")
                    m = pkg_model(name=name, repo=repo, branch=branch, arch=arch, last_update=update)
                    m.save()
                
            elif "%VERSION%" in item:
                version = next(it).decode().strip() 
                m = pkg_model.objects.get(name=name)

                if "unstable" in branch:
                    m.unstable=version
                elif "testing" in branch:
                    m.testing=version         
                elif "stable" in branch:
                    m.stable=version
                m.save()
    except StopIteration:
        pass
            

def parse_db(arch, branch, repos, pkg_model, last_update_model):
    for repo in repos:
        pkg_model.objects.filter(arch=arch, branch=branch, repo=repo).delete()
        file = get_db(arch, branch, repo, last_update_model)
        if file:
            tf = tarfile.open(fileobj=file, mode='r:gz')
            try:
                while True:
                    member = tf.next()
                    if member is None:
                        break
                    if not member.isfile():
                        continue
                    fileobj = tf.extractfile(member)
                    if fileobj:
                        parse_pkg_desc(fileobj, branch, repo, pkg_model, arch)                    
            finally:
                tf.close()

def build_db(arch, branches, repos, pkg_model, last_update_model):
    print(f"{arch}:: starting job ...")
    start = time.perf_counter()
    try:
        pkg_model.objects.all().delete()
        last_update_model.objects.all().delete()
        for branch in branches:
            parse_db(arch, branch, repos, pkg_model, last_update_model)
    finally:
        hours, rem = divmod(time.perf_counter() - start, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"{arch}:: build_db end : {hours:.0f} {minutes:.0f}:{seconds:.0f}")



def update_packages(pkg_model, last_update_model):
    arch = "x86_64"
    branches = ("stable", "testing", "unstable")
    repos = ("multilib", "core", "extra", "community", "kde-unstable")
    # branches = ("stable",)
    # repos = ("core",)
    updateday = date.today().strftime("%B %d, %Y")

    #build_db(arch, branches, repos, pkg_model, last_update_model)  old version
    dl = Downloader(Archs.x86_64, branches, repos)
    if repos := dl.run():

        db = AlpmDb(Archs.x86_64, repos)
        db.parse_files()

        # start real db update
        start = time.perf_counter()
        try:
            print(f"sql update {arch} :: start - all packages in:", repos)
            print(f"sql update {arch} :: for {len(db.pkgs)} packages")
            for repo in repos:
                pkg_model.objects.filter(arch=arch, repo=repo).delete()
            pkg: PackageAlpm
            objs = []
            for _, pkg in db.pkgs.items():
                try:
                    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-create
                    objs.append(pkg_model(
                        name=pkg.name,
                        repo=pkg.repo,
                        # branch = #FIXME no raison to exists ?
                        arch=arch,
                        stable=pkg.version(Branches.stable),
                        testing=pkg.version(Branches.testing),
                        unstable=pkg.version(Branches.unstable),
                        group=pkg.groups,
                        url=pkg.url,
                        packager=pkg.packager_name,
                        builddate=pkg.builddate_str,
                        last_update=updateday))
                except:
                    print(pkg, pkg.packager_name, pkg.builddate_str, )
                    raise
            ret = len(pkg_model.objects.bulk_create(objs))
            print(ret)
        finally:
            hours, rem = divmod(time.perf_counter() - start, 3600)
            minutes, seconds = divmod(rem, 60)
            print(f"sql update{arch} :: end {hours:.0f} {minutes:.0f}:{seconds:.0f}")
        # TODO remove:    CACHE_DIR / arch


def update_arm_packages(pkg_model, last_update_model):
    return
    arch = "aarch64"
    branches = ("arm-stable", "arm-testing", "arm-unstable")
    repos = ("core", "extra", "community", "kde-unstable", "mobile")
    build_db(arch, branches, repos, pkg_model, last_update_model)  
