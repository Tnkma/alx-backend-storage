#!/usr/bin/python3
""" writing strings to Redis"""
import redis
import uuid
from typing import Union


class Cache:
    """ Cache class """
    def __init__(self) -> None:
        """ constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store data in redis """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
