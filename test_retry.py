





"""
Final test script for retry mechanism
"""
import logging
import time
from utils.retry import RetryManager, retry
from custom_exceptions import RetryableError, NonRetryableError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_retry_basic():
    """Test basic retry functionality"""
    print("=== Testing Basic Retry ===")

    retry_manager = RetryManager(max_attempts=3, initial_delay=0.1)

    # Test successful call
    def successful_call():
        return "success"

    result = retry_manager.call(successful_call)
    assert result == "success"
    print("✅ Successful call works correctly")

    # Test retryable failure
    attempt_count = 0

    def retryable_failure():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:  # Succeed on 3rd attempt (3rd try)
            raise RetryableError(f"Retryable failure attempt {attempt_count}")
        return "success after retries"

    result = retry_manager.call(retryable_failure)
    assert result == "success after retries"
    assert attempt_count == 3
    print("✅ Retryable failures handled correctly")

    # Test non-retryable failure
    def non_retryable_failure():
        raise NonRetryableError("This should not be retried")

    try:
        retry_manager.call(non_retryable_failure)
        assert False, "Should have raised NonRetryableError"
    except NonRetryableError:
        print("✅ Non-retryable exceptions not retried")

def test_retry_decorator():
    """Test retry decorator"""
    print("\n=== Testing Retry Decorator ===")

    attempt_count = 0

    @retry(max_attempts=2, initial_delay=0.1, retry_exceptions=(RuntimeError,))
    def unreliable_function():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 2:
            raise RuntimeError(f"Decorator retry attempt {attempt_count}")
        return "decorator success"

    result = unreliable_function()
    assert result == "decorator success"
    assert attempt_count == 2
    print("✅ Retry decorator works correctly")

def test_retry_exponential_backoff():
    """Test exponential backoff"""
    print("\n=== Testing Exponential Backoff ===")

    start_time = time.time()
    retry_manager = RetryManager(
        max_attempts=4,
        initial_delay=0.1,
        backoff_factor=2.0,
        max_delay=1.0,
        retry_exceptions=(RuntimeError,)
    )

    attempt_count = 0

    def failing_function():
        nonlocal attempt_count
        attempt_count += 1
        raise RuntimeError("Always fails")

    try:
        retry_manager.call(failing_function)
    except RuntimeError:
        pass  # Expected

    end_time = time.time()
    elapsed = end_time - start_time

    # Should have waited approximately 0.1 + 0.2 + 0.4 + 0.8 = 1.5 seconds
    # With some jitter and execution time
    print(f"Elapsed time: {elapsed:.2f}s, attempt count: {attempt_count}")
    # More lenient assertion since we have jitter
    assert elapsed >= 0.5 and elapsed <= 2.5
    assert attempt_count == 4
    print(f"✅ Exponential backoff works correctly (elapsed: {elapsed:.2f}s)")

def test_retry_custom_exceptions():
    """Test custom retry exceptions"""
    print("\n=== Testing Custom Retry Exceptions ===")

    retry_manager = RetryManager(
        max_attempts=2,
        retry_exceptions=(RetryableError,),
        non_retry_exceptions=(NonRetryableError,)
    )

    # Test retryable exception
    attempt_count = 0

    def retryable_exception():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 2:
            raise RetryableError("Should be retried")
        return "retryable success"

    result = retry_manager.call(retryable_exception)
    assert result == "retryable success"
    assert attempt_count == 2
    print("✅ Custom retryable exceptions work correctly")

    # Test non-retryable exception
    def non_retryable_exception():
        raise NonRetryableError("Should not be retried")

    try:
        retry_manager.call(non_retryable_exception)
        assert False, "Should have raised NonRetryableError"
    except NonRetryableError:
        print("✅ Custom non-retryable exceptions work correctly")

def test_retry_max_attempts():
    """Test max attempts limit"""
    print("\n=== Testing Max Attempts ===")

    retry_manager = RetryManager(max_attempts=3, initial_delay=0.1, retry_exceptions=(ValueError,))

    attempt_count = 0

    def always_failing():
        nonlocal attempt_count
        attempt_count += 1
        raise ValueError("Always fails")

    try:
        retry_manager.call(always_failing)
        assert False, "Should have raised ValueError"
    except ValueError:
        assert attempt_count == 3
        print("✅ Max attempts limit enforced correctly")

if __name__ == "__main__":
    test_retry_basic()
    test_retry_decorator()
    test_retry_exponential_backoff()
    test_retry_custom_exceptions()
    test_retry_max_attempts()
    print("\n🎉 All retry tests completed successfully!")





