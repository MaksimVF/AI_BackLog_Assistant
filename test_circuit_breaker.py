



"""
Test script for circuit breaker implementation
"""
import logging
import time
from utils.circuit_breaker import CircuitBreaker, circuit_breaker, get_circuit_breaker
from custom_exceptions import CircuitBreakerError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_circuit_breaker_basic():
    """Test basic circuit breaker functionality"""
    print("=== Testing Basic Circuit Breaker ===")

    # Create a circuit breaker
    cb = CircuitBreaker("test-service", max_failures=2, reset_timeout=5)

    # Test successful calls
    def successful_call():
        return "success"

    result = cb.call(successful_call)
    assert result == "success"
    assert cb.state == "closed"
    print("✅ Successful call works correctly")

    # Test failure handling
    failure_count = 0

    def failing_call():
        nonlocal failure_count
        failure_count += 1
        if failure_count <= 2:
            raise ValueError("Simulated failure")
        return "success after failures"

    try:
        cb.call(failing_call)
    except ValueError:
        pass  # Expected

    assert cb.state == "closed"
    assert cb._failure_count == 1
    print("✅ First failure handled correctly")

    try:
        cb.call(failing_call)
    except ValueError:
        pass  # Expected

    assert cb.state == "open"
    assert cb._failure_count == 2
    print("✅ Circuit opened after max failures")

    # Test circuit open behavior
    try:
        cb.call(successful_call)
        assert False, "Should have raised CircuitBreakerError"
    except CircuitBreakerError:
        print("✅ Circuit breaker prevents calls when open")

    # Wait for reset
    time.sleep(6)  # Wait for reset timeout + 1 second

    # Test reset
    result = cb.call(successful_call)
    assert result == "success"
    assert cb.state == "closed"
    print("✅ Circuit reset successfully")

def test_circuit_breaker_decorator():
    """Test circuit breaker decorator"""
    print("\n=== Testing Circuit Breaker Decorator ===")

    failure_count = 0

    @circuit_breaker("decorator-test", max_failures=2, reset_timeout=3)
    def unreliable_function():
        nonlocal failure_count
        failure_count += 1
        if failure_count <= 2:
            raise RuntimeError("Simulated decorator failure")
        return "decorator success"

    # Test failures
    try:
        unreliable_function()
    except RuntimeError:
        pass  # Expected

    try:
        unreliable_function()
    except RuntimeError:
        pass  # Expected

    # Get the circuit breaker instance
    cb = get_circuit_breaker("decorator-test")
    assert cb.state == "open"
    print("✅ Decorator opens circuit after failures")

    # Wait for reset
    time.sleep(4)  # Wait for reset timeout + 1 second

    # Test successful call after reset
    result = unreliable_function()
    assert result == "decorator success"
    assert cb.state == "closed"
    print("✅ Decorator reset works correctly")

def test_circuit_breaker_half_open():
    """Test half-open state behavior"""
    print("\n=== Testing Half-Open State ===")

    cb = CircuitBreaker("half-open-test", max_failures=1, reset_timeout=2)

    def failing_call():
        raise ConnectionError("Simulated connection error")

    def successful_call():
        return "half-open success"

    # Trigger circuit open
    try:
        cb.call(failing_call)
    except ConnectionError:
        pass

    assert cb.state == "open"
    print("✅ Circuit opened after failure")

    # Wait for reset attempt
    time.sleep(3)  # Wait for reset timeout + 1 second

    # Test successful reset
    result = cb.call(successful_call)
    assert result == "half-open success"
    assert cb.state == "closed"
    print("✅ Half-open state reset successfully")

    # Test failed reset
    cb = CircuitBreaker("failed-reset-test", max_failures=1, reset_timeout=2)

    # Trigger circuit open
    try:
        cb.call(failing_call)
    except ConnectionError:
        pass

    time.sleep(3)  # Wait for reset

    # Test failed reset (should go back to open)
    try:
        cb.call(failing_call)
    except ConnectionError:
        pass

    assert cb.state == "open"
    print("✅ Failed reset returns to open state")

def test_circuit_breaker_registry():
    """Test circuit breaker registry"""
    print("\n=== Testing Circuit Breaker Registry ===")

    # Get or create circuit breakers
    cb1 = get_circuit_breaker("registry-test-1")
    cb2 = get_circuit_breaker("registry-test-1")  # Should return same instance
    cb3 = get_circuit_breaker("registry-test-2")

    assert cb1 is cb2
    assert cb1 is not cb3
    print("✅ Circuit breaker registry works correctly")

    # Test different configurations
    cb4 = get_circuit_breaker("config-test", max_failures=5, reset_timeout=10)
    assert cb4.max_failures == 5
    assert cb4.reset_timeout == 10
    print("✅ Circuit breaker configuration works correctly")

if __name__ == "__main__":
    test_circuit_breaker_basic()
    test_circuit_breaker_decorator()
    test_circuit_breaker_half_open()
    test_circuit_breaker_registry()
    print("\n🎉 All circuit breaker tests completed successfully!")


