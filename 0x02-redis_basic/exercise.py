#!/usr/bin/env python3
""" writing strings to Redis"""
import redis
import uuid
from typing import Union, Optional, Callable


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

    def get(self, key: str, fn: Optional[Callable] =
            None) -> Union[str, bytes, int, float, None]:
        """ get data from redis

        Args:
            key (str): the key to get
            fn (Optional[Callable], optional): used to convert the data.

        Returns:
            Union[str, bytes, int, float, None]: _description_
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """ get string from redis """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """ get int from redis """
        return self.get(key, lambda d: int(d))
