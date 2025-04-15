import time
import asyncio
import functools

def retry(max_tries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(max_tries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if i < max_tries - 1:
                        print(f"⚠️ Retry ({i+1}) for {func.__name__} due to error: {e}")
                        await asyncio.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator
