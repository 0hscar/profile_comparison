print("timing_utils.py loaded")
import time
import logging
from functools import wraps

def timeit(label):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            logging.info(f"{label} took {duration:.3f} seconds")
            return result
        return wrapper
    return decorator
