from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse
from functools import lru_cache as cache
from .utils import (
    do_task,
    check_blacklist,
    sort_alphabetically,
    get_tabs
)

@cache(maxsize=128)
def search(request):
    import time
    start = time.time()
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
        search_results.extend(do_task(query, _type))

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

        
        end = time.time()
        print(end - start)
        return TemplateResponse(request, 'search/search.html', {
            "search_query": " OR ".join(queries),
            "tabs": get_tabs(results),
            "search_results": results,
            "total": len(search_results)
        })

    
