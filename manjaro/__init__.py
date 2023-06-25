from requests_cache import CachedSession

session_requests = CachedSession(backend="memory", allowable_methods=('GET'), cache_control=True)