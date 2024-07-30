#!/usr/bin/env python3
"""Web caching with Redis"""
import redis
import requests
from typing import Callable
from functools import wraps

def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache the result"""
    cache = redis.Redis()
    cache_key = f"count:{url}"
    cache.incr(cache_key)
    
    content_key = f"cached:{url}"
    content = cache.get(content_key)
    
    if content:
        return content.decode('utf-8')
    
    response = requests.get(url)
    content = response.text
    cache.setex(content_key, 10, content)
    
    return content