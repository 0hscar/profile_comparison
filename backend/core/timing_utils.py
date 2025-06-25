import time
import logging
from functools import wraps

def timeit(label):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logging.info(f"{label} - {func.__name__}: {elapsed_time:.4f} seconds")
            return result
        return wrapper
    return decorator
