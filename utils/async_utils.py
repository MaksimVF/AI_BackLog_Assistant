



"""
Async Processing Utilities
"""

import asyncio
import concurrent.futures
from typing import Any, Awaitable, Callable, Coroutine, List, Optional, TypeVar, Union
from functools import wraps

T = TypeVar('T')

def run_sync_in_executor(func: Callable[..., T]) -> Callable[..., Coroutine[Any, Any, T]]:
    """
    Decorator to run synchronous functions in an executor to avoid blocking the event loop.

    Args:
        func: Synchronous function to convert to async

    Returns:
        Async function that runs the original function in an executor
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        loop = asyncio.get_event_loop()
        # Use a thread pool executor for CPU-bound tasks
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, func, *args, **kwargs)
    return wrapper

async def gather_with_concurrency(limit: int, *tasks: Awaitable[T]) -> List[T]:
    """
    Run async tasks with concurrency limit.

    Args:
        limit: Maximum number of concurrent tasks
        *tasks: Awaitable tasks to run

    Returns:
        List of results from completed tasks
    """
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task: Awaitable[T]) -> T:
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))

async def run_with_timeout(
    coroutine: Awaitable[T],
    timeout: float,
    default: Optional[T] = None
) -> Optional[T]:
    """
    Run a coroutine with a timeout.

    Args:
        coroutine: Coroutine to run
        timeout: Timeout in seconds
        default: Default value to return if timeout occurs

    Returns:
        Result of the coroutine or default value if timeout occurs
    """
    try:
        return await asyncio.wait_for(coroutine, timeout=timeout)
    except asyncio.TimeoutError:
        return default

def async_retry(
    retries: int = 3,
    delay: float = 0.1,
    backoff: float = 2.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
):
    """
    Async retry decorator with exponential backoff.

    Args:
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier for delay
        exceptions: Exception types to catch and retry

    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            current_attempt = 0
            current_delay = delay

            while current_attempt <= retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    current_attempt += 1
                    if current_attempt > retries:
                        raise

                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

class AsyncPipelineProcessor:
    """
    Helper class for processing pipeline stages asynchronously
    """

    def __init__(self, concurrency_limit: int = 5):
        self.concurrency_limit = concurrency_limit

    async def process_stages(
        self,
        data: Any,
        stages: List[Callable[[Any], Awaitable[Any]]]
    ) -> Any:
        """
        Process data through a series of async stages.

        Args:
            data: Input data to process
            stages: List of async processing functions

        Returns:
            Processed data
        """
        result = data
        for stage in stages:
            result = await stage(result)
        return result

    async def process_parallel_stages(
        self,
        data: Any,
        stages: List[Callable[[Any], Awaitable[Any]]]
    ) -> List[Any]:
        """
        Process data through parallel async stages.

        Args:
            data: Input data to process
            stages: List of async processing functions

        Returns:
            List of results from each stage
        """
        tasks = [stage(data) for stage in stages]
        return await gather_with_concurrency(self.concurrency_limit, *tasks)



