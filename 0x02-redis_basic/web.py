#!/usr/bin/env python3
"""Web caching with Redis"""
import redis
import requests
from datetime import timedelta
from functools import wraps
from typing import Callable

def cache_and_count(func: Callable) -> Callable:
    """Decorator to cache the result and count accesses of a URL"""
    @wraps(func)
    def wrapper(url: str) -> str:
        if url is None or len(url.strip()) == 0:
            return ''
        
        cache = redis.Redis()
        res_key = f'result:{url}'
        req_key = f'count:{url}'
        
        # Check if the result is already cached
        result = cache.get(res_key)
        if result is not None:
            # Increment the request count if the result is cached
            cache.incr(req_key)
            return result.decode('utf-8')
        
        # Fetch the result if not cached
        result = func(url)
        
        # Cache the result with an expiration time of 10 seconds
        cache.setex(res_key, timedelta(seconds=10), result)
        
        # Increment the request count
        cache.incr(req_key)
        
        return result
    return wrapper

@cache_and_count
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache the result"""
    response = requests.get(url)
    return response.text