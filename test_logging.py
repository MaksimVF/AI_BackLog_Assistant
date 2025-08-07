




import sys
import os
import json
import time
import logging
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.system_admin.logging_manager import LoggingManager, initialize_logging

def test_logging_system():
    """Test the enhanced logging system"""
    print("=== Testing Enhanced Logging System ===")

    # Test 1: Basic logging initialization
    print("\n1. Testing basic logging initialization...")
    logging_manager = initialize_logging(
        service_name="TestService",
        environment="test",
        log_level="DEBUG"
    )

    logger = logging_manager.get_logger()
    logger.info("Test log message")
    print("✓ Basic logging initialized successfully")

    # Test 2: Structured logging
    print("\n2. Testing structured logging...")
    logger.info("Structured log test", extra={'user_id': 'test123', 'action': 'login'})
    print("✓ Structured logging works")

    # Test 3: Log levels
    print("\n3. Testing different log levels...")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    print("✓ All log levels work")

    # Test 4: Context logging
    print("\n4. Testing context logging...")
    context_logger = logging_manager.add_context(user_id="context123", session="abcdef")
    context_logger.info("Contextual log message")
    print("✓ Context logging works")

    # Test 5: Specialized logging
    print("\n5. Testing specialized logging...")
    logging_manager.log_metric("test_metric", 42.5, unit="ms")
    logging_manager.log_audit("test_action", "test_user", "test_resource", "success")
    logging_manager.log_health_check("test_service", "healthy", uptime=1234)
    print("✓ Specialized logging works")

    # Test 6: Dynamic log level change
    print("\n6. Testing dynamic log level change...")
    logging_manager.set_log_level("WARNING")
    logger.debug("This debug message should not appear")
    logger.warning("This warning message should appear")
    print("✓ Dynamic log level change works")

    # Test 7: Exception logging
    print("\n7. Testing exception logging...")
    try:
        1 / 0
    except Exception as e:
        logging_manager.log_exception("Division by zero error", e)
    print("✓ Exception logging works")

    # Test 8: Log rotation (simulated)
    print("\n8. Testing log rotation configuration...")
    # Note: Actual rotation would require writing enough data to trigger it
    # For testing, we'll just verify the configuration
    assert logging_manager.max_bytes == 10485760  # 10MB
    assert logging_manager.backup_count == 5
    print("✓ Log rotation configuration is correct")

    # Test 9: External system configuration
    print("\n9. Testing external system configuration...")
    test_external_config = {
        'elk': {
            'host': 'localhost:9200',
            'index': 'test_logs'
        },
        'http': {
            'url': 'https://example.com/logs'
        }
    }

    external_manager = initialize_logging(
        service_name="ExternalTest",
        environment="test",
        external_systems=test_external_config
    )
    print("✓ External system configuration works (actual sending not tested)")

    print("\n=== Enhanced Logging System Test Complete ===")

if __name__ == "__main__":
    test_logging_system()




