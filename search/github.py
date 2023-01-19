from github import Github
import os, datetime
from .models import SearchData, SearchLastUpdate
from django.db.models import Q
from django.utils.text import Truncator
from functools import lru_cache as cache

@cache(maxsize=128)
def _build_github_search_data(org, results=[]):
    if os.getenv('GITHUB_TOKEN'):
        gh = Github(os.getenv('GITHUB_TOKEN'))
    else:
        gh = Github()

    repos = gh.get_organization(org).get_repos()    
    for item in repos:
        if not item.archived:
            repo_result = {
                "url": item.html_url,
                "title": item.name,
                "description": "",
                "is_doc": False,
                "type": "repository",
                "message": "repository"
                }
            if item.description:
                repo_result["description"] = Truncator(item.description).chars(160)
            results.append(repo_result) 
            if item.has_issues:
                for issue in item.get_issues():
                    if "pull" not in item.html_url:
                        repo_result = {
                        "url": issue.html_url,
                        "title": issue.title,
                        "description": Truncator(issue.body).chars(160),
                        "is_doc": False,
                        "type": "issue",
                        "message": "issue",
                        "state": issue.state
                        }
                    results.append(repo_result)  
    return tuple(results)

@cache(maxsize=128)
def _check_github_needs_updating(org):
    time_now = datetime.datetime.now().astimezone()
    update_frequency = 58
    try:
        last_update = SearchLastUpdate.objects.get(id=1)
    except SearchLastUpdate.DoesNotExist:
        SearchLastUpdate(
            time = time_now - datetime.timedelta(minutes=update_frequency+1)
        ).save()
        last_update = SearchLastUpdate.objects.get(id=1)

    if last_update.time + datetime.timedelta(minutes=update_frequency) <= time_now:
        print("Updating github data")
        last_update.time = time_now
        last_update.save()
        if org == "manjaro":
            SearchData.objects.all().delete()
        results = _build_github_search_data(org)
        for result in results:
            try:
                data = SearchData.objects.create(
                    url=result["url"],
                    title=result["title"],
                    description=result["description"],
                    type=result["type"],
                    message=result["message"]
                )
                if result["state"]:
                    data.state = result["state"]
                data.save()
            except Exception as e:
                print(e)
    else:
        print("Github already up to date")


@cache(maxsize=128)
def get_github_results(search_query, org):
    _check_github_needs_updating(org)    
    results = SearchData.objects.filter(
        Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    search_results = []
    for result in results:
        page_result = {
            "url": result.url,
            "title": result.title,
            "description": result.description,
            "is_doc": result.is_doc,
            "type": result.type,
            "message": result.message,
            "state": result.state
        }
        search_results.append(page_result)
    return tuple(search_results)

def get_manjaro_results(search_query):
    return get_github_results(search_query, "manjaro")

def get_sway_results(search_query):
    return get_github_results(search_query, "manjaro-sway")

def get_gnome_results(search_query):
    return get_github_results(search_query, "manjaro-gnome")

def get_plasma_results(search_query):
    return get_github_results(search_query, "manjaro-plasma")

def get_xfce_results(search_query):
    return get_github_results(search_query, "manjaro-xfce")
