import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
cache = redis.Redis()


def get_page(url: str) -> str:
    """ Fetches the content of a web page and caches it for 10 seconds """
    cache_key = f"count:{url}"
    cached_content_key = f"content:{url}"

    # Increment the access count for the URL
    cache.incr(cache_key)

    # Try to get the cached content
    cached_content = cache.get(cached_content_key)
    if cached_content:
        return cached_content.decode('utf-8')

    # If not cached, fetch the content from the URL
    response = requests.get(url)
    content = response.text

    # Cache the content with an expiration time of 10 seconds
    cache.setex(cached_content_key, 10, content)

    return content


# Bonus: Implementing with decorators
def cache_page(fn: Callable) -> Callable:
    """ Caches the content of a web page for 10 seconds """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper function to cache the content of a web page """
        cache_key = f"count:{url}"
        cached_content_key = f"content:{url}"

        # Increment the access count for the URL
        cache.incr(cache_key)

        # Try to get the cached content
        cached_content = cache.get(cached_content_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # If not cached, fetch the content from the URL
        content = fn(url)

        # Cache the content with an expiration time of 10 seconds
        cache.setex(cached_content_key, 10, content)

        return content
    return wrapper


@cache_page
def get_page_with_decorator(url: str) -> str:
    """ Fetches the content of a web page and caches it for 10 seconds """
    response = requests.get(url)
    return response.text
