

#!/usr/bin/env python3
"""
Integration test for the new configuration and error handling system.
This demonstrates how the new components work together in a real application.
"""

import os
import sys
import config.settings_new as settings
from utils.retry import RetryManager, retry
from utils.circuit_breaker import CircuitBreaker, circuit_breaker
from custom_exceptions import RetryableError, NonRetryableError

def test_configuration_integration():
    """Test that the new configuration system works with the application"""
    print("📋 Testing Configuration Integration")
    print("=" * 50)

    print(f"✅ Redis URL: {settings.REDIS_URL}")
    print(f"✅ Weaviate URL: {settings.WEAVIATE_URL}")
    print(f"✅ Log Level: {settings.LOG_LEVEL}")
    print(f"✅ Secret Key: {settings.SECRET_KEY[:10]}...")
    print(f"✅ Access Token Expire Minutes: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")

    # Test that configuration validation works
    try:
        from config.advanced_config import config
        print(f"✅ Configuration schema validation successful")
        print(f"   - ClickHouse host: {config.config.clickhouse.host}")
        print(f"   - ClickHouse port: {config.config.clickhouse.port}")
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

    return True

def test_retry_integration():
    """Test retry mechanism in a real scenario"""
    print("\n🔁 Testing Retry Mechanism Integration")
    print("=" * 50)

    retry_manager = RetryManager(max_attempts=3, initial_delay=0.1)

    attempt_count = 0

    def unreliable_database_call():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            print(f"   Attempt {attempt_count}: Database connection failed")
            raise RetryableError(f"Database connection failed (attempt {attempt_count})")
        print(f"   Attempt {attempt_count}: Database connection successful")
        return {"status": "success", "data": "sample_data"}

    try:
        result = retry_manager.call(unreliable_database_call)
        print(f"✅ Retry successful: {result}")
        assert result["status"] == "success"
        assert attempt_count == 3
        return True
    except Exception as e:
        print(f"❌ Retry failed: {e}")
        return False

def test_circuit_breaker_integration():
    """Test circuit breaker in a real scenario"""
    print("\n🛡️  Testing Circuit Breaker Integration")
    print("=" * 50)

    circuit_breaker = CircuitBreaker(
        name="external-api",
        max_failures=2,
        reset_timeout=5
    )

    failure_count = 0

    def unreliable_api_call():
        nonlocal failure_count
        failure_count += 1
        if failure_count <= 2:
            print(f"   Call {failure_count}: API request failed")
            raise RuntimeError(f"API request failed (call {failure_count})")
        print(f"   Call {failure_count}: API request successful")
        return {"status": "success", "result": "api_data"}

    # First call should work (but will fail)
    try:
        result = circuit_breaker.call(unreliable_api_call)
        print(f"   First call result: {result}")
    except Exception as e:
        print(f"   First call failed: {e}")

    # Second call should work (but will fail and open circuit)
    try:
        result = circuit_breaker.call(unreliable_api_call)
        print(f"   Second call result: {result}")
    except Exception as e:
        print(f"   Second call failed: {e}")

    # Third call should be blocked by circuit breaker
    try:
        result = circuit_breaker.call(unreliable_api_call)
        print(f"   Third call result: {result}")
    except Exception as e:
        print(f"   Third call blocked: {e}")

    print(f"   Circuit breaker state: {circuit_breaker.state}")
    return True

def test_decorator_integration():
    """Test retry decorator in a real scenario"""
    print("\n🎯 Testing Retry Decorator Integration")
    print("=" * 50)

    attempt_count = 0

    @retry(max_attempts=2, initial_delay=0.1, retry_exceptions=(RuntimeError,))
    def process_document(document_id):
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 2:
            print(f"   Document processing attempt {attempt_count} failed")
            raise RuntimeError(f"Document processing failed (attempt {attempt_count})")
        print(f"   Document processing attempt {attempt_count} successful")
        return {"document_id": document_id, "status": "processed"}

    try:
        result = process_document("doc_123")
        print(f"✅ Document processing successful: {result}")
        assert result["document_id"] == "doc_123"
        assert result["status"] == "processed"
        assert attempt_count == 2
        return True
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Running Integration Tests")
    print("=" * 50)

    tests = [
        test_configuration_integration,
        test_retry_integration,
        test_circuit_breaker_integration,
        test_decorator_integration,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")

    print(f"\n📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All integration tests passed!")
        return 0
    else:
        print("❌ Some integration tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

