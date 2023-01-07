from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse
from wagtail.models import Page
from wagtail.search.models import Query
import requests, re
from mediawiki import MediaWiki
import concurrent.futures


def get_forum_results(query):
    URL = "https://forum.manjaro.org/"
    endpoint = f"{URL}/search.json"
    response = requests.get(endpoint, params={
        "q": query,
        "order":"latest",
        "status": "public",
        "in": "title",
        "in": "first"
    }, timeout=3.50 )
    if response.ok:
        search_results = []
        response = response.json()
        try:
            topics = response["topics"]
            posts = response["posts"]
            for topic in topics:
                topic_result = {
                "url": f"{URL}t/{topic['slug']}",
                "title": re.sub("[\[].*?[\]]", "", topic["title"]),
                "description": "",
                "is_doc": False,
                "type": "forum"
                }
                # shoud we exclude any forum categories?
                if topic["category_id"] == 40: # tutorials
                    topic_result["is_doc"] = True
                for post in posts:
                    if post["topic_id"] == topic["id"]:
                        topic_result["description"] = post["blurb"]
                search_results.append(topic_result)
        except KeyError:
            pass        
        return search_results

def get_software_results(query):
    URL = "https://software.manjaro.org/"
    endpoint = f"{URL}/search.json"
    response = requests.get(endpoint, params={
        "query": query,
    }, timeout=3.50 )
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

def get_wiki_search_results(query):
    url = "https://wiki.manjaro.org/"
    endpoint = "api.php"
    wiki = MediaWiki(url=f"{url}{endpoint}")
    search = wiki.search(query)
    search_results = []
    for page in search:
        # do not add same page in multiples languages
        if "/" not in page:
            p = wiki.page(page)
            description = p.summarize(chars=150)
            page_result = {
            "url": f"{url}index.php/{p.title.replace(' ', '_')}",
            "title": p.title,
            "description": description,
            "is_doc": True,
            "type": "wiki"
            } 
            # do not add existing pages
            if page_result["url"] not in (p["url"] for p in search_results):
                if description:
                    search_results.append(page_result)
    return search_results 

def search(request):
    search_query = request.GET.get('query', None)
    format = request.GET.get('format', None)
    futures = []
    results = []
    search_providers = (
        get_forum_results,
        get_wiki_search_results,
        get_page_results,
        get_software_results
        )
    with concurrent.futures.ThreadPoolExecutor(len(search_providers)) as executor:
        for provider in search_providers:
            futures.append(executor.submit(provider, search_query))
        for future in concurrent.futures.as_completed(futures):
            try:
                results.extend(future.result())
            except Exception as e:
                print(e)

    has_docs = False
    for result in results:
        if result["is_doc"]:
            has_docs = True
            break

    search_results = sorted(tuple(results), key=lambda i: i['title'])
    if format == "json":
        data = {
            "Status": HttpResponse.status_code,
            "results-found": len(search_results),
            "Content-Type": "application/json",
            "search-results": search_results
        }
        return JsonResponse(data, safe=False)
    else:
        return TemplateResponse(request, 'search/search.html', {
            "search_query": search_query,
            "search_results": search_results,
            "has_docs": has_docs,
            "results_found": len(search_results),
        })
