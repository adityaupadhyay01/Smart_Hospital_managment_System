import functools
from datetime import datetime

def log_action(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  [LOG {ts}] {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  [LOG {ts}] Done: {func.__name__}")
        return result
    return wrapper
