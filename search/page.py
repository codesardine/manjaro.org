from wagtail.models import Page
from wagtail.search.models import Query
from functools import lru_cache as cache

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