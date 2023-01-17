from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse
from wagtail.models import Page
from wagtail.search.models import Query
import requests, re
from mediawiki import MediaWiki
import concurrent.futures
from django.utils.text import Truncator
import gitlab, os, datetime
from .models import SearchData, SearchLastUpdate
from django.db.models import Q
from github import Github
import asyncio
from functools import lru_cache as cache


headers = {
    "User-Agent": "Manjaro-Starter 1.0 (+https://manjaro.org)"
}

@cache(maxsize=128)
def get_query(search_query, _type):
        pkg_formats = ("appimage", "package", "snap", "flatpak", "packages")
        results = []
        search_providers = []
        if _type:
            for provider in _type.split(" "):
                if provider in pkg_formats:
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
                    search_providers.append(get_github_results)
        else:
            search_providers.append(get_software_results)
            search_providers.append(get_forum_results)
            search_providers.append(get_wiki_results)
            search_providers.append(get_page_results)
            search_providers.append(get_gitlab_hosted_projects_results)
            search_providers.append(get_gitlab_hosted_issues_results)
            search_providers.append(get_github_results)

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


def sort_alphabetically(results):
    return sorted(tuple(results), key=lambda i: i['title'])


@cache(maxsize=128)
def get_forum_results(query):
    URL = "https://forum.manjaro.org/"
    endpoint = f"{URL}/search.json"
    response = requests.get(endpoint, params={
        "q": query,
        "order":"latest",
        "status": "public",
        "in": "title"
    }, timeout=4, headers=headers)
    if response.ok:
        search_results = []
        response = response.json()
        try:
            topics = response["topics"]
            posts = response["posts"]
            for topic in topics:
                excluded_categories = [120]
                if topic["visible"] and topic["category_id"] not in excluded_categories:
                    topic_result = {
                    "url": f"{URL}t/{topic['slug']}",
                    "title": re.sub("[\[].*?[\]]", "", topic["title"]),
                    "description": "",
                    "is_doc": False,
                    "type": "forum",
                    "activity": topic["posts_count"] + topic["reply_count"],
                    "message": "unsolved"
                    }
                    if topic["tags"]:
                        tags = []
                        for tag in topic["tags"]:
                            tags.append(tag)
                        topic_result["tags"] = tags
                    announcements = [11, 19, 12, 15, 13, 18, 79, 80, 81, 102, 101, 112]
                    if topic["category_id"] == 40: # tutorials
                        topic_result["is_doc"] = True
                        topic_result["message"] = "Tutorial"
                    elif topic["category_id"] in announcements:
                        topic_result["message"] = None
                    elif topic["has_accepted_answer"]:
                        topic_result["message"] = "solved"
                    for post in posts:
                        if post["topic_id"] == topic["id"]:
                            topic_result["description"] = Truncator(post["blurb"]).chars(160)
                    search_results.append(topic_result)
        except KeyError:
            pass        
        return tuple(search_results)


@cache(maxsize=128)
def get_software_results(query, _type):
    URL = "https://software.manjaro.org/"
    endpoint = f"{URL}/search.json"
    params={
        "query": query,
    }
    if _type:
        if _type == "packages":
            _type = "snap appimage package flatpak"        
        else:
            params["type"] = _type
    response = requests.get(endpoint, params, timeout=4, headers=headers)
    if response.ok:
        response = response.json()            
        return tuple(response)


@cache(maxsize=128)
def get_page_results(search_query):
        search_results = []
        if search_query:
            results = Page.objects.live().public().search(search_query)
            query = Query.get(search_query)
            query.add_hit()
        else:
            results = Page.objects.none()    

        for result in results:
            page_result = {
            "url": str(result.url),
            "title": result.title,
            "description": result.search_description,
            "is_doc": False,
            "type": "page"
            }
            if "docs." in page_result["url"]:
                page_result["is_doc"] = True
            
            search_results.append(page_result)
        return tuple(search_results)


@cache(maxsize=128)
def get_wiki_results(query):
    url = "https://wiki.manjaro.org/"
    endpoint = "api.php"
    wiki = MediaWiki(url=f"{url}{endpoint}", user_agent=headers["User-Agent"])
    search = wiki.search(query)
    search_results = []
    for page in search:
        # do not add same page in multiples languages
        if "/" not in page:
            p = wiki.page(page)
            description = p.summarize(chars=160)
            page_result = {
            "url": f"{url}index.php/{p.title.replace(' ', '_')}",
            "title": p.title,
            "description": description,
            "is_doc": True,
            "type": "wiki",
            "links": []
            } 
            for link in p.links:
                links = {
                    "url": f"{url}index.php/{link.replace(' ', '_')}",
                    "title": link,
                    "description": wiki.page(link).summarize(chars=160)
                }
                page_result["links"].append(links)
            # do not add existing pages
            if page_result["url"] not in (p["url"] for p in search_results):
                if description:
                    search_results.append(page_result)
    return tuple(search_results) 


@cache(maxsize=128)
def get_gitlab_hosted_projects_results(search_query):
    gl = gitlab.Gitlab(
        url='https://gitlab.manjaro.org',
        private_token=os.getenv('GITLAB_HOSTED_TOKEN'),
        user_agent=headers["User-Agent"]
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


@cache(maxsize=128)
def get_gitlab_hosted_issues_results(search_query):
    gl = gitlab.Gitlab(
        url='https://gitlab.manjaro.org',
        private_token=os.getenv('GITLAB_HOSTED_TOKEN'),
        user_agent=headers["User-Agent"]
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


def _build_github_search_data():
    orgs = ("manjaro", "manjaro-sway", "manjaro-plasma", "manjaro-gnome")
    results = []

    async def task_org(org):
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
    
    async def main():
        tasks = [task_org(org) for org in orgs]
        await asyncio.gather(*tasks)
       
    asyncio.run(main())
    return tuple(results)


def _check_github_needs_updating():
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
        SearchData.objects.all().delete()
        results = _build_github_search_data()
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
def get_github_results(search_query):
    _check_github_needs_updating()    
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


@cache(maxsize=128)
def search(request):
    search_query = request.GET.get('query', None)
    _type = request.GET.get('type', None)
    _format = request.GET.get('format', None)
    queries = []
    search_results = []
    term_blacklist = []

    if "NOT" in search_query:
        term_blacklist.append(search_query.split("NOT")[1].strip())
        search_query = search_query.split("NOT")[0].strip()

    if "AND" in search_query:
        _type = search_query.split("AND")[1].strip()
        search_query = search_query.split("AND")[0].strip()

    if "OR" in search_query:
        queries.append(search_query.split("OR")[1].strip())
        queries.append(search_query.split("OR")[0].strip())
    else:
        queries.append(search_query)

    for query in queries:
        search_results.extend(get_query(query, _type))

    search_results = check_blacklist(search_results, term_blacklist)
    if _format == "json":
        data = {
            "Status": HttpResponse.status_code,
            "results-found": len(search_results),
            "Content-Type": "application/json",
            "search-results": search_results
        }
        return JsonResponse(data, safe=False)
    else:
        results = {}
        results["documentation"] = []
        results["forum"] = []
        results["pages"] = []
        results["git"] = []
        results["packages"] = []
        for item in search_results:
            if item["is_doc"]:
                results["documentation"].append(item)
            elif item["type"] == "forum":
                results["forum"].append(item)
            elif item["type"] == "page":
                results["pages"].append(item)
            elif item["type"] == "issue" or item["type"] == "repository":
                results["git"].append(item)
            elif item["type"] == "snap" or item["type"] == "package" or item["type"] == "appimage" or item["type"] == "snap":
                results["packages"].append(item)
        
        results["documentation"] = sort_alphabetically(results["documentation"])
        results["git"] = sort_alphabetically(results["git"])
        results["packages"] = sort_alphabetically(results["packages"])

        tabs = (
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

        return TemplateResponse(request, 'search/search.html', {
            "search_query": " OR ".join(queries),
            "tabs": tabs,
            "search_results": results,
            "total": len(search_results)
        })

    
