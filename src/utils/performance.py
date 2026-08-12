import time
from functools import wraps
from src.utils.logger import logger

def measure_performance(operation: str):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = function(
                *args,
                **kwargs
            )

            end = time.perf_counter()
            elapsed = (end - start) * 1000
            if elapsed < 100:
                status = "🟢 FAST"
            elif elapsed < 1000:
                status = "🟡 NORMAL"
            else:
                status = "🔴 SLOW"
                
            if elapsed < 1000:
                duration = f"{elapsed:.2f} ms"
            else:
                duration = f"{elapsed / 1000:.2f} sec"

            logger.info(
                f"{operation} completed in {duration}"
)

            return result
        return wrapper
    return decorator