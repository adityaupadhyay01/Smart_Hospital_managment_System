# utils/decorators.py — Reusable decorators

import functools
from datetime import datetime

def log_action(func):
    """Decorator that logs every action with a timestamp."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  [LOG {timestamp}] Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  [LOG {timestamp}] Completed: {func.__name__}")
        return result
    return wrapper