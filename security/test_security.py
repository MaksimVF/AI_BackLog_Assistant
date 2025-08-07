









import os
import sys
import unittest
import json
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.security_system import SecuritySystem, SecurityLevel, SecurityConfig

class TestSecuritySystem(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.security = SecuritySystem()

    def test_encryption_decryption(self):
        """Test data encryption and decryption"""
        test_data = {"message": "Hello, secure world!", "timestamp": datetime.utcnow().isoformat()}

        # Test encryption
        encrypted = self.security.encrypt_data(test_data)
        self.assertIsInstance(encrypted, str)
        self.assertNotEqual(encrypted, json.dumps(test_data))

        # Test decryption
        decrypted = self.security.decrypt_data(encrypted)
        self.assertEqual(decrypted, test_data)

    def test_hmac(self):
        """Test HMAC generation and verification"""
        test_data = "Test message for HMAC"

        # Test HMAC generation
        hmac_signature = self.security.generate_hmac(test_data)
        self.assertIsInstance(hmac_signature, str)
        self.assertEqual(len(hmac_signature), 64)  # SHA-256 produces 64-char hex

        # Test HMAC verification
        is_valid = self.security.verify_hmac(test_data, hmac_signature)
        self.assertTrue(is_valid)

        # Test with wrong signature
        wrong_signature = "0" * 64
        is_valid = self.security.verify_hmac(test_data, wrong_signature)
        self.assertFalse(is_valid)

    def test_token_generation_verification(self):
        """Test token generation and verification"""
        payload = {"user_id": "123", "role": "admin", "email": "user@example.com"}

        # Test token generation
        token = self.security.generate_token(payload, security_level=SecurityLevel.HIGH)
        self.assertIsInstance(token, str)
        self.assertIn(".", token)

        # Test token verification
        verified_payload = self.security.verify_token(token)
        self.assertEqual(verified_payload["user_id"], "123")
        self.assertEqual(verified_payload["role"], "admin")

        # Test expired token
        expired_token = self.security.generate_token(payload, expiration=-3600)
        with self.assertRaises(ValueError):
            self.security.verify_token(expired_token)

    def test_api_key_management(self):
        """Test API key generation and verification"""
        # Test API key generation
        api_key = self.security.generate_api_key("test_service", SecurityLevel.MEDIUM)
        self.assertIsInstance(api_key, str)
        self.assertTrue(api_key.startswith("TES_MED_"))

        # Test API key verification
        security_level = self.security.verify_api_key(api_key)
        self.assertEqual(security_level, SecurityLevel.MEDIUM)

        # Test invalid API key
        with self.assertRaises(ValueError):
            self.security.verify_api_key("invalid_key")

    def test_ip_allowlist(self):
        """Test IP allowlist checking"""
        # Test allowed IP
        is_allowed = self.security.check_ip_allowlist("127.0.0.1")
        self.assertTrue(is_allowed)

        # Test disallowed IP
        is_allowed = self.security.check_ip_allowlist("8.8.8.8")
        self.assertFalse(is_allowed)

    def test_rsa_encryption(self):
        """Test RSA encryption and decryption"""
        # Generate RSA keys
        keys = self.security.generate_rsa_keys()
        public_key = keys["public_key"]
        private_key = keys["private_key"]

        # Test encryption
        test_message = "Secret message for RSA"
        encrypted = self.security.rsa_encrypt(test_message, public_key)
        self.assertIsInstance(encrypted, str)

        # Test decryption
        decrypted = self.security.rsa_decrypt(encrypted, private_key)
        self.assertEqual(decrypted.decode(), test_message)

    def test_secure_hashing(self):
        """Test secure password hashing"""
        password = "secure_password_123!"

        # Test hashing
        hashed = self.security.secure_hash(password)
        self.assertIsInstance(hashed, str)
        self.assertIn("$", hashed)

        # Test verification
        is_valid = self.security.verify_hash(password, hashed)
        self.assertTrue(is_valid)

        # Test wrong password
        is_valid = self.security.verify_hash("wrong_password", hashed)
        self.assertFalse(is_valid)

    def test_component_communication(self):
        """Test secure component communication"""
        message = {"command": "process_data", "data": [1, 2, 3, 4, 5]}

        # Test secure message creation
        secure_message = self.security.secure_component_communication(
            message, "agent1", "agent2"
        )
        self.assertIn("source", secure_message)
        self.assertIn("target", secure_message)
        self.assertIn("timestamp", secure_message)
        self.assertIn("hmac", secure_message)

        # Test message verification
        verified_message = self.security.verify_component_message(
            secure_message,
            expected_source="agent1",
            expected_target="agent2"
        )
        self.assertEqual(verified_message, message)

        # Test with wrong source
        with self.assertRaises(ValueError):
            self.security.verify_component_message(
                secure_message,
                expected_source="wrong_source",
                expected_target="agent2"
            )

    def test_configuration_loading(self):
        """Test security configuration loading"""
        # Test default config loading
        default_config = self.security._load_default_config()
        self.assertIsInstance(default_config, SecurityConfig)
        self.assertTrue(default_config.encryption_enabled)
        self.assertTrue(default_config.hmac_enabled)

        # Test config validation
        try:
            self.security._validate_config()
        except ValueError:
            self.fail("Config validation raised ValueError unexpectedly")

    def test_disabled_security_features(self):
        """Test behavior when security features are disabled"""
        # Create config with disabled features
        disabled_config = SecurityConfig(
            encryption_enabled=False,
            hmac_enabled=False
        )

        disabled_security = SecuritySystem(disabled_config)

        # Test encryption disabled
        with self.assertRaises(ValueError):
            disabled_security.encrypt_data("test")

        # Test HMAC disabled
        with self.assertRaises(ValueError):
            disabled_security.generate_hmac("test")

if __name__ == "__main__":
    unittest.main()










