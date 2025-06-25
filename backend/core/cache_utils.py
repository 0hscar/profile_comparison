import re
from django.core.cache import cache
from django.http import JsonResponse
import functools
import hashlib
import json

def safe_cache_key(key):
    """
    Generate a safe cache key by replacing any characters that are not alphanumeric, underscore, or hyphen with an underscore.
    """
    return re.sub(r'[^a-zA-Z0-9_-]', '_', key)


def check_for_cached_data(key):
    """
    Check if data is cached for the given key.
    """
    data = cache.get(safe_cache_key(key))
    if data:
        return data
    else:
        print(f"No cached data found for key: {key}")
        return False

def set_cached_data(key, data, timeout=60*60):
    """
    Set cached data for the given key with an optional timeout (default 1 hour).
    """
    cache.set(safe_cache_key(key), data, timeout)


def cache_generator_response(key_func):
    """
    Decorator to cache the output of a generator function as a list.
    key_func should accept the same arguments as the decorated function and return a cache key string.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = key_func(*args, **kwargs)
            cached = check_for_cached_data(cache_key)
            if cached:
                for chunk in cached:
                    yield chunk
                return
            chunks = []
            for chunk in func(*args, **kwargs):
                chunks.append(chunk)
                yield chunk
            set_cached_data(cache_key, chunks)
        return wrapper
    return decorator
