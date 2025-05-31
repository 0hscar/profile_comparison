import re

def safe_cache_key(key):
    # Replace any character not alphanumeric or _ or - with _
    return re.sub(r'[^a-zA-Z0-9_-]', '_', key)
