import gitlab, os
from django.utils.text import Truncator
from . import get_headers
from functools import lru_cache as cache


@cache(maxsize=128)
def get_gitlab_hosted_projects_results(search_query):
    gl = gitlab.Gitlab(
        url='https://gitlab.manjaro.org',
        private_token=os.getenv('GITLAB_HOSTED_TOKEN'),
        user_agent=get_headers()["User-Agent"]
        )

    projects = gl.search(gitlab.const.SearchScope.PROJECTS, search_query, iterator=True)
    search_results = []
    for item in projects:
        page_result = {
            "url": item["web_url"],
            "title": item["name"],
            "description": Truncator(item["description"]).chars(160),
            "is_doc": False,
            "type": "repository",
            "message": "repository"
            }
        search_results.append(page_result)
    return tuple(search_results)


#@cache(maxsize=128)
def get_gitlab_hosted_issues_results(search_query):
    gl = gitlab.Gitlab(
        url='https://gitlab.manjaro.org',
        private_token=os.getenv('GITLAB_HOSTED_TOKEN'),
        user_agent=get_headers()["User-Agent"]
        )

    issues = gl.search(gitlab.const.SearchScope.ISSUES, search_query, iterator=True)
    search_results = []
    for item in issues:
        page_result = {
            "url": item["web_url"],
            "title": item["title"],
            "description": Truncator(item["description"]).chars(160),
            "is_doc": False,
            "type": "issue",
            "message": "issue",
            "state": item["state"]
            }
        search_results.append(page_result)        
    return tuple(search_results)