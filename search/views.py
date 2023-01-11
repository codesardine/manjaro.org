from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse
from wagtail.models import Page
from wagtail.search.models import Query
import requests, re
from mediawiki import MediaWiki
import concurrent.futures
from django.utils.text import Truncator

headers = {
    "User-Agent": "Manjaro-Search-Bot 1.0 (+https://manjaro.org)"
}

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
        else:
            search_providers.append(get_software_results)
            search_providers.append(get_forum_results)
            search_providers.append(get_wiki_results)
            search_providers.append(get_page_results)

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

def sort_search_results(results, terms_blacklist):
    if terms_blacklist:
        search_results = []
        for result in results:
            test_case = f'{result["title"]} {result["description"]} {result["url"]}'
            if any(term.lower() not in test_case.lower() for term in terms_blacklist):
                search_results.append(result)
    else:
        search_results = results        
                
    r = sorted(search_results, key=lambda i: i['title'])
    return sorted(tuple(r), key=lambda i: i['is_doc'] == False)

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
                            desc = Truncator(post["blurb"])
                            topic_result["description"] = desc.chars(160)
                    search_results.append(topic_result)
        except KeyError:
            pass        
        return search_results

def get_software_results(query, _type):
    URL = "https://software.manjaro.org/"
    endpoint = f"{URL}/search.json"
    params={
        "query": query,
    }
    if _type:
        params["type"] = _type
    response = requests.get(endpoint, params, timeout=4, headers=headers)
    if response.ok:
        response = response.json()            
        return response

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
        return search_results

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
                    "description": Truncator(wiki.page(link).summarize(chars=160))
                }
                page_result["links"].append(links)
            # do not add existing pages
            if page_result["url"] not in (p["url"] for p in search_results):
                if description:
                    search_results.append(page_result)
    return search_results 

def search(request):
    search_query = request.GET.get('query', None)
    _type = request.GET.get('type', None)
    _format = request.GET.get('format', None)
    if _type == "packages":
            _type = "appimage snap flatpak package"
    queries = []
    search_results = []
    term_blacklist = []

    if "NOT" in search_query:
        term_blacklist.append(search_query.split("NOT")[1].strip())
        search_query = search_query.split("NOT")[0].strip()

    if "AND" in search_query:
        _type = search_query.split("AND")[1].strip()
        if _type == "packages":
            _type = "appimage snap flatpak package"
        search_query = search_query.split("AND")[0].strip()

    if "OR" in search_query:
        queries.append(search_query.split("OR")[1].strip())
        queries.append(search_query.split("OR")[0].strip())
    else:
        queries.append(search_query)

    for query in queries:
        search_results.extend(get_query(query, _type))

    search_results = sort_search_results(search_results, term_blacklist)
    if _format == "json":
        data = {
            "Status": HttpResponse.status_code,
            "results-found": len(search_results),
            "Content-Type": "application/json",
            "search-results": search_results
        }
        return JsonResponse(data, safe=False)
    else:
        return TemplateResponse(request, 'search/search.html', {
            "search_query": " AND ".join(queries),
            "search_results": search_results,
            "results_found": len(search_results),
        })

    
