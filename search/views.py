from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from wagtail.models import Page
from wagtail.search.models import Query
import requests
from mediawiki import MediaWiki


URL = "https://forum.manjaro.org/"

def get_forum_results(query):
    endpoint = f"{URL}/search.json"
    response = requests.get(endpoint, params={
        "q": query,
        "order":"latest",
        "status": "public",
        "in": "title",
        "in": "first"
    })
    if response.ok:
        search_results = []
        response = response.json()
        topics = response["topics"]
        posts = response["posts"]
        for topic in topics:
            topic_result = {
            "url": f"{URL}t/{topic['slug']}",
            "title": topic["title"],
            "description": ""
            }
            for post in posts:
                if post["topic_id"] == topic["id"]:
                    topic_result["description"] = post["blurb"]
            search_results.append(topic_result)
        return search_results

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
            "description": result.search_description
            }            
            search_results.append(page_result)
        return search_results

def get_wiki_search_results(query):
    url = "https://wiki.manjaro.org/"
    endpoint = "api.php"
    wiki = MediaWiki(url=f"{url}{endpoint}")
    search = wiki.search(query)
    search_results = []
    for page in search:
        if "/" not in page:
            p = wiki.page(page)
            description = p.summarize(chars=150)
            page_result = {
            "url": f"{url}index.php/{p.title.replace(' ', '_')}",
            "title": p.title,
            "description": description
            } 
            if description:
                search_results.append(page_result)
    return search_results 

def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)
    forum_results = get_forum_results(search_query)
    website_results  = get_page_results(search_query)
    wiki_results = get_wiki_search_results(search_query)
    results = []
    has_docs = False
    if wiki_results:
        has_docs = True
        results.extend(wiki_results)

    if forum_results:
        results.extend(forum_results)

    if website_results:
        for result in website_results:
            if "docs" in result["url"]:
                has_docs = True
        results.extend(website_results)

    search_results = sorted(results, key=lambda i: i['title'])
    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': tuple(search_results),
        'has_docs': has_docs,
    })
