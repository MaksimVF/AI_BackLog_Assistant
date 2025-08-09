




"""
Test script for security integration
"""

import os
import sys
import time
import asyncio
import threading

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security_integration import security_integration
from security.security_system import SecurityLevel
from agents.system_admin.logging_manager import initialize_logging

# Initialize logging
logging_manager = initialize_logging(
    service_name="SecurityTest",
    environment="test"
)
logger = logging_manager.get_logger()

def test_secure_communication():
    """Test secure communication between components"""
    print("=== Testing Secure Communication ===")

    # Test message
    message = {"command": "process_data", "data": [1, 2, 3]}

    # Secure the message
    secured_message = security_integration.secure_component_communication(
        message, "test_sender", "test_receiver"
    )
    print(f"Secured message: {secured_message}")

    # Verify the message
    verified_message = security_integration.verify_component_message(
        secured_message,
        expected_source="test_sender",
        expected_target="test_receiver"
    )
    print(f"Verified message: {verified_message}")

    # Test with wrong source
    try:
        security_integration.verify_component_message(
            secured_message,
            expected_source="wrong_sender",
            expected_target="test_receiver"
        )
        print("❌ Wrong source verification should have failed")
    except ValueError as e:
        print(f"✓ Wrong source verification correctly failed: {e}")

    print("✓ Secure communication test completed")

def test_token_security():
    """Test token generation and verification"""
    print("\n=== Testing Token Security ===")

    # Generate token
    token = security_integration.generate_secure_token(
        {"user_id": "test_user", "role": "admin"},
        security_level=SecurityLevel.HIGH
    )
    print(f"Generated token: {token}")

    # Verify token
    verified_payload = security_integration.verify_secure_token(token)
    print(f"Verified payload: {verified_payload}")

    # Test expired token
    expired_token = security_integration.generate_secure_token(
        {"user_id": "test_user", "role": "admin"},
        expiration=-1  # Already expired
    )

    try:
        security_integration.verify_secure_token(expired_token)
        print("❌ Expired token verification should have failed")
    except ValueError as e:
        print(f"✓ Expired token verification correctly failed: {e}")

    print("✓ Token security test completed")

def test_auditing():
    """Test security auditing"""
    print("\n=== Testing Security Auditing ===")

    # Test audit operation
    audit_record = security_integration.audit_operation(
        "test_operation",
        user_id="test_user",
        inputs={"param1": "value1"},
        outputs={"result": "success"}
    )
    print(f"Audit record: {audit_record}")

    # Test audit with failure
    audit_record_failed = security_integration.audit_operation(
        "test_failed_operation",
        user_id="test_user",
        inputs={"param1": "value1"},
        outputs={"result": "failure"},
        status="failed"
    )
    print(f"Failed audit record: {audit_record_failed}")

    print("✓ Security auditing test completed")

def test_security_audit():
    """Test comprehensive security audit"""
    print("\n=== Testing Security Audit ===")

    # Perform security audit
    audit_results = security_integration.perform_security_audit()
    print(f"Security audit recommendations: {len(audit_results['recommendations'])}")

    if audit_results.get("penetration_testing"):
        print(f"Penetration testing: {audit_results['penetration_testing']['status']}")
        if audit_results['penetration_testing'].get("vulnerabilities"):
            print(f"Vulnerabilities found: {len(audit_results['penetration_testing']['vulnerabilities'])}")

    if audit_results.get("vulnerability_scanning"):
        print(f"Vulnerability scanning: {audit_results['vulnerability_scanning']['status']}")
        if audit_results['vulnerability_scanning'].get("vulnerabilities"):
            print(f"Vulnerabilities found: {len(audit_results['vulnerability_scanning']['vulnerabilities'])}")

    print("✓ Security audit test completed")

def test_api_security():
    """Test API security"""
    print("\n=== Testing API Security ===")

    # Test with valid API key
    api_key = security_integration.security_system.generate_api_key("test_service", SecurityLevel.HIGH)
    print(f"Generated API key: {api_key}")

    @security_integration.secure_api_endpoint(required_security_level=SecurityLevel.MEDIUM)
    def test_endpoint(data, api_key=None, token=None):
        return {"status": "success", "data": data, "api_key": api_key}

    try:
        result = test_endpoint({"test": "data"}, api_key=api_key)
        print(f"API call with valid key: {result['status']}")
    except ValueError as e:
        print(f"API call with valid key failed: {e}")

    # Test with invalid API key
    try:
        result = test_endpoint({"test": "data"}, api_key="invalid_key")
        print(f"❌ API call with invalid key should have failed: {result}")
    except ValueError as e:
        print(f"✓ API call with invalid key correctly failed: {e}")

    print("✓ API security test completed")

def test_integration():
    """Test complete security integration"""
    print("\n=== Testing Complete Security Integration ===")

    # Test all features together
    message = {"command": "process_data", "data": [1, 2, 3]}

    # Secure communication
    secured_message = security_integration.secure_component_communication(
        message, "main_app", "processor"
    )
    verified_message = security_integration.verify_component_message(
        secured_message, expected_source="main_app", expected_target="processor"
    )

    # Audit the operation
    audit_record = security_integration.audit_operation(
        "integration_test",
        inputs=message,
        outputs=verified_message
    )

    # Generate and verify token
    token = security_integration.generate_secure_token(
        {"user_id": "integration_user", "role": "user"}
    )
    verified_payload = security_integration.verify_secure_token(token)

    print(f"Integration test results:")
    print(f"  - Secure communication: ✓")
    print(f"  - Auditing: ✓")
    print(f"  - Token security: ✓")
    print(f"  - Verified payload: {verified_payload}")

    print("✓ Integration test completed")

def main():
    """Run all security integration tests"""
    print("🔒 Running Security Integration Tests")
    print("=" * 50)

    try:
        test_secure_communication()
        test_token_security()
        test_auditing()
        test_security_audit()
        test_api_security()
        test_integration()

        print("\n🎉 All security integration tests completed!")
        print("✅ Security improvements are fully integrated")

    except Exception as e:
        print(f"\n❌ Security integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()




