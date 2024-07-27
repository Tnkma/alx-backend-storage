#!/usr/bin/env python3
""" Redis Module """
from functools import wraps
import redis
import requests
from typing import Callable
from datetime import timedelta


def get_page(url: str) -> str:
    """ Get page count"""
    if url is None or len(url.strip()) == 0:
        return ''
    redis = redis.Redis()
    res_key = 'result:{}'.format(url)
    req_key = 'count:{}'.format(url)
    result = redis.get(res_key)
    if result is not None:
        redis.incr(req_key)
        return result
    result = requests.get(url).content.decode('utf-8')
    redis.setex(res_key, timedelta(seconds=10), result)
    return result