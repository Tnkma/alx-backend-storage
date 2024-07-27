import requests
import redis
from functools import wraps
from time import sleep


cache = redis.Redis(host='localhost', port=6379, db=0)

def cache_page(func):
    """ Caches the page content for 10 seconds """
    @wraps(func)
    def wrapper(url):
        """ Wrapper for decorator functionality """
        # Key for counting accesses
        count_key = f"count:{url}"
        # Key for caching the page content
        cache_key = f"cache:{url}"

        # Increment the access count
        cache.incr(count_key)

        # Try to get the cached page
        cached_page = cache.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')

        # If not cached, call the function and cache the result
        result = func(url)
        cache.setex(cache_key, 10, result)  # Cache for 10 seconds
        return result
    return wrapper

@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text