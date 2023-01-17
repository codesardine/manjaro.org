from mediawiki import MediaWiki
from . import get_headers
from functools import lru_cache as cache

@cache(maxsize=128)
def get_wiki_results(query):
    url = "https://wiki.manjaro.org/"
    endpoint = "api.php"
    wiki = MediaWiki(url=f"{url}{endpoint}", user_agent=get_headers()["User-Agent"])
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