#!/usr/bin/env python3
""" Redis Module """

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis connection
redis_ = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """Decorator for counting requests and caching results"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper for decorator"""
        # Increment the request count
        redis_.incr(f"count:{url}")

        # Check if the response is cached
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # If not cached, fetch the page
        html = method(url)

        # Cache the response with an expiration time of 10 seconds
        redis_.setex(f"cached:{url}", 10, html)
        return html

    return wrapper

@count_requests
def get_page(url: str) -> str:
    """Obtain the HTML content of a URL"""
    req = requests.get(url)
    return req.text
