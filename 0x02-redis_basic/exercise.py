#!/usr/bin/env python3
""" writing strings to Redis"""
import redis
import uuid
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ keeps track of the number of times a method is called"""

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """ increments the count for a method every time it is called"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """ stores the history of inputs and outputs for a method"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):  # sourcery skip: avoid-builtin-shadow
        """ Wrapper for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(fn: Callable) -> None:
    """ display the history of calls of a particular function"""
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))

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
