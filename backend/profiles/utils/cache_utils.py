import re
from django.core.cache import cache
from django.http import JsonResponse

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

def get_cached_and_uncached(restaurants, key_func):
    """
    Given a list of restaurant dicts and a function to generate cache keys,
    returns a tuple (cached, uncached) where:
      - cached: list of restaurant dicts found in cache
      - uncached: list of restaurant dicts not found in cache
    """
    cached = []
    uncached = []
    for r in restaurants:
        cache_key = key_func(r)
        cached_data = cache.get(cache_key)
        if cached_data and 'user_restaurant' in cached_data:
            cached.append(cached_data['user_restaurant'])
        else:
            uncached.append(r)
    return cached, uncached

def cache_given_list(restaurants: list, key_func, timeout=60*60):
    """
    Cache a list of restaurant dicts using a key function to generate cache keys.
    """
    for r in restaurants:
        cache_key = key_func(r)
        set_cached_data(cache_key, {"user_restaurant": r}, timeout=timeout)
