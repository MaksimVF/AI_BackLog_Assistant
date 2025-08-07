




"""
Retry mechanism for resilient operations
"""
import time
import logging
from typing import Callable, Optional, Any, List, Union, Type, Tuple
from functools import wraps
from custom_exceptions import RetryableError, NonRetryableError

logger = logging.getLogger(__name__)

class RetryManager:
    """
    Retry manager for resilient operations
    """

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 0.1,
        backoff_factor: float = 2.0,
        max_delay: float = 10.0,
        retry_exceptions: Optional[Union[List[Type[Exception]], Tuple[Type[Exception], ...]]] = None,
        non_retry_exceptions: Optional[Union[List[Type[Exception]], Tuple[Type[Exception], ...]]] = None
    ):
        """
        Initialize retry manager

        Args:
            max_attempts: Maximum number of retry attempts
            initial_delay: Initial delay between retries in seconds
            backoff_factor: Multiplier for exponential backoff
            max_delay: Maximum delay between retries in seconds
            retry_exceptions: List of exception types to retry
            non_retry_exceptions: List of exception types not to retry
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.retry_exceptions = retry_exceptions or (RetryableError,)
        self.non_retry_exceptions = non_retry_exceptions or (NonRetryableError,)

    def _should_retry(self, exception: Exception) -> bool:
        """Determine if an exception should be retried"""
        # Don't retry non-retryable exceptions
        if isinstance(exception, self.non_retry_exceptions):
            return False

        # Retry specific exceptions if specified
        if self.retry_exceptions:
            return isinstance(exception, self.retry_exceptions)

        # Default: retry all exceptions except non-retryable
        return True

    def _get_delay(self, attempt: int) -> float:
        """Calculate delay for exponential backoff"""
        delay = min(self.initial_delay * (self.backoff_factor ** (attempt - 1)), self.max_delay)
        # Add some jitter to avoid thundering herd
        jitter = delay * 0.1  # 10% jitter
        return delay + (jitter * ((attempt * 13) % 21 - 10) / 10)  # Random-ish jitter

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with retry logic

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result of function call

        Raises:
            Exception: If all retries fail
        """
        last_exception = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                if attempt > 1:
                    delay = self._get_delay(attempt - 1)
                    logger.debug(f"Retry attempt {attempt}/{self.max_attempts} after {delay:.2f}s delay")
                    time.sleep(delay)

                logger.debug(f"Executing attempt {attempt}")
                result = func(*args, **kwargs)
                logger.debug(f"Attempt {attempt} succeeded")
                return result

            except Exception as e:
                last_exception = e
                logger.debug(f"Attempt {attempt} caught exception: {type(e).__name__}: {str(e)}")

                if not self._should_retry(e):
                    logger.debug(f"Not retrying {type(e).__name__}: {str(e)}")
                    break

                logger.warning(f"Attempt {attempt} failed: {type(e).__name__}: {str(e)}")

                # Continue to next attempt unless we've reached max attempts
                if attempt >= self.max_attempts:
                    logger.debug(f"Reached max attempts ({self.max_attempts})")
                    break

                # Continue to next attempt
                continue

        # All retries failed
        logger.debug("All retries failed, raising exception")
        if last_exception:
            raise last_exception
        else:
            raise RuntimeError("Operation failed after maximum retries")

    def decorator(self, func: Callable) -> Callable:
        """
        Decorator version of retry manager

        Args:
            func: Function to decorate

        Returns:
            Wrapped function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper

def retry(
    max_attempts: int = 3,
    initial_delay: float = 0.1,
    backoff_factor: float = 2.0,
    max_delay: float = 10.0,
    retry_exceptions: Optional[Union[List[Type[Exception]], Tuple[Type[Exception], ...]]] = None,
    non_retry_exceptions: Optional[Union[List[Type[Exception]], Tuple[Type[Exception], ...]]] = None
):
    """
    Decorator factory for retry logic

    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for exponential backoff
        max_delay: Maximum delay between retries in seconds
        retry_exceptions: List of exception types to retry
        non_retry_exceptions: List of exception types not to retry

    Returns:
        Decorator function
    """
    def decorator(func):
        retry_manager = RetryManager(
            max_attempts=max_attempts,
            initial_delay=initial_delay,
            backoff_factor=backoff_factor,
            max_delay=max_delay,
            retry_exceptions=retry_exceptions,
            non_retry_exceptions=non_retry_exceptions
        )
        return retry_manager.decorator(func)
    return decorator




