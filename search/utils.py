import concurrent.futures
from functools import lru_cache as cache
from .software import get_software_results
from .wiki import get_wiki_results
from .forum import get_forum_results
from .page import get_page_results
from .gitlab import (
    get_gitlab_hosted_issues_results,
    get_gitlab_hosted_projects_results)
from .github import (
    get_manjaro_results,
    get_sway_results)
    #get_gnome_results,
    #get_plasma_results,
    #get_xfce_results)


def get_tabs(results):
    return (
            {
              "name": "documentation",
              "total": len(results["documentation"]),
            },
            {
              "name": "forum",
              "total": len(results["forum"]),
            },
            {
              "name": "pages", 
              "total": len(results["pages"]),
            },
            {
              "name": "git",
              "total": len(results["git"]),
            },
            {
              "name": "packages",
              "total": len(results["packages"]),
            }
        )

@cache(maxsize=128)
def do_task(search_query, _type):
        pkg_types = ("appimage", "package", "snap", "flatpak", "packages")
        results = []
        search_providers = []
        if _type:
            for provider in _type.split(" "):
                if provider in pkg_types:
                    search_providers.append(get_software_results)
                if provider == "forum":
                    search_providers.append(get_forum_results)
                if provider == "wiki":
                    search_providers.append(get_wiki_results)
                if provider == "page":
                    search_providers.append(get_page_results)
                if provider == "git":
                    search_providers.append(get_gitlab_hosted_projects_results)
                    search_providers.append(get_gitlab_hosted_issues_results)
                    search_providers.append(get_manjaro_results)
                    #search_providers.append(get_gnome_results)
                    #search_providers.append(get_plasma_results)
                    search_providers.append(get_sway_results)
                    #search_providers.append(get_xfce_results)
        else:
            search_providers.append(get_software_results)
            search_providers.append(get_forum_results)
            search_providers.append(get_wiki_results)
            search_providers.append(get_page_results)
            search_providers.append(get_gitlab_hosted_projects_results)
            search_providers.append(get_gitlab_hosted_issues_results)
            search_providers.append(get_manjaro_results)
            #search_providers.append(get_gnome_results)
            #search_providers.append(get_plasma_results)
            search_providers.append(get_sway_results)
            #search_providers.append(get_xfce_results)

        with concurrent.futures.ThreadPoolExecutor(10) as executor:
            futures = []
            for provider in search_providers:
                if provider == get_software_results:
                    futures.append(executor.submit(provider, search_query, _type))
                else:
                    futures.append(executor.submit(provider, search_query))
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.extend(future.result())
                except Exception as e:
                    print(e)
        return results

def check_blacklist(results, terms_blacklist):
    if terms_blacklist:
        search_results = []
        for result in results:
            test_case = f'{result["title"]} {result["description"]} {result["url"]}'
            if any(term.lower() not in test_case.lower() for term in terms_blacklist):
                search_results.append(result)
    else:
        search_results = results        
    return search_results

def sort_alphabetically(results, reverse=False, sort_by="title"):
    return sorted(tuple(results), key=lambda i: i[sort_by], reverse=reverse)
