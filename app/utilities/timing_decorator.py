import time
from functools import wraps

def timeit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time
        result = await func(*args, **kwargs)  # Await the async function
        end_time = time.time()  # End time
        execution_time = end_time - start_time  # Calculate the execution time
        print(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")
        return result

    return wrapper