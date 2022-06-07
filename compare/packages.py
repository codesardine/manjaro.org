import requests
import tarfile
import time
from datetime import date
from dateutil.parser import parse as parsedate

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
    print("starting job...")
    start = time.time()
    pkg_model.objects.all().delete()
    last_update_model.objects.all().delete()
    for branch in branches:
       parse_db(arch, branch, repos, pkg_model, last_update_model)        
    print(time.time() - start)


def update_packages(pkg_model, last_update_model):
    arch = "x86_64"
    branches = ("stable", "testing", "unstable")
    repos = ("multilib", "core", "extra", "community", "kde-unstable")
    build_db(arch, branches, repos, pkg_model, last_update_model)


def update_arm_packages(pkg_model, last_update_model):
    arch = "aarch64"
    branches = ("arm-stable", "arm-testing", "arm-unstable")
    repos = ("core", "extra", "community", "kde-unstable", "mobile")
    build_db(arch, branches, repos, pkg_model, last_update_model)  
