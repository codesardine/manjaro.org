import requests
from . import get_headers
from functools import lru_cache as cache


#@cache(maxsize=128)
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
    response = requests.get(endpoint, params, timeout=4, headers=get_headers())
    if response.ok:
        response = response.json()            
        return tuple(response)