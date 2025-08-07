








import os
import sys
import json
import logging
import hashlib
import hmac
import base64
import secrets
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.config_manager import ConfigManager

# Initialize logging
logging_manager = initialize_logging(
    service_name="SecuritySystem",
    environment=os.getenv('ENV', 'dev')
)

class SecurityLevel(Enum):
    """Security levels for different operations"""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

@dataclass
class SecurityConfig:
    """Security configuration"""
    encryption_enabled: bool = True
    encryption_key: Optional[str] = None
    hmac_enabled: bool = True
    hmac_key: Optional[str] = None
    token_expiration: int = 3600  # 1 hour in seconds
    token_secret: Optional[str] = None
    api_keys: Dict[str, SecurityLevel] = field(default_factory=dict)
    allowed_ips: List[str] = field(default_factory=list)
    rate_limits: Dict[str, int] = field(default_factory=dict)

class SecuritySystem:
    """Security system for secure communication between components"""

    def __init__(self, config: Optional[SecurityConfig] = None):
        """Initialize security system"""
        self.config = config or self._load_default_config()
        self.config_manager = ConfigManager()
        self._validate_config()

        # Generate keys if not provided
        if self.config.encryption_enabled and not self.config.encryption_key:
            self.config.encryption_key = Fernet.generate_key().decode()

        if self.config.hmac_enabled and not self.config.hmac_key:
            self.config.hmac_key = secrets.token_hex(32)

        if not self.config.token_secret:
            self.config.token_secret = secrets.token_hex(32)

        # Initialize cryptographic components
        self.fernet = Fernet(self.config.encryption_key.encode()) if self.config.encryption_enabled else None

    def _load_default_config(self) -> SecurityConfig:
        """Load default security configuration"""
        return SecurityConfig(
            encryption_enabled=True,
            hmac_enabled=True,
            token_expiration=3600,
            api_keys={
                "default_api_key": SecurityLevel.MEDIUM
            },
            allowed_ips=["127.0.0.1", "::1"],
            rate_limits={
                "login": 5,  # 5 attempts per minute
                "api": 100   # 100 requests per minute
            }
        )

    def _validate_config(self):
        """Validate security configuration"""
        if not self.config:
            raise ValueError("Security configuration not provided")

        if self.config.encryption_enabled and not self.config.encryption_key:
            logging.warning("Encryption enabled but no key provided - generating new key")

        if self.config.hmac_enabled and not self.config.hmac_key:
            logging.warning("HMAC enabled but no key provided - generating new key")

        if not self.config.token_secret:
            logging.warning("No token secret provided - generating new secret")

    def encrypt_data(self, data: Union[str, bytes, Dict[str, Any]]) -> str:
        """Encrypt data using Fernet symmetric encryption"""
        if not self.config.encryption_enabled:
            raise ValueError("Encryption is not enabled")

        if isinstance(data, dict):
            data_str = json.dumps(data)
        elif isinstance(data, str):
            data_str = data
        elif isinstance(data, bytes):
            data_str = data.decode()
        else:
            raise ValueError("Unsupported data type for encryption")

        encrypted = self.fernet.encrypt(data_str.encode())
        return encrypted.decode()

    def decrypt_data(self, encrypted_data: str) -> Union[str, Dict[str, Any]]:
        """Decrypt data using Fernet symmetric encryption"""
        if not self.config.encryption_enabled:
            raise ValueError("Encryption is not enabled")

        decrypted = self.fernet.decrypt(encrypted_data.encode())

        try:
            # Try to parse as JSON
            return json.loads(decrypted.decode())
        except json.JSONDecodeError:
            # Return as string
            return decrypted.decode()

    def generate_hmac(self, data: Union[str, bytes]) -> str:
        """Generate HMAC for data integrity"""
        if not self.config.hmac_enabled:
            raise ValueError("HMAC is not enabled")

        if isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = data

        hmac_obj = hmac.new(
            self.config.hmac_key.encode(),
            data_bytes,
            hashlib.sha256
        )
        return hmac_obj.hexdigest()

    def verify_hmac(self, data: Union[str, bytes], signature: str) -> bool:
        """Verify HMAC signature"""
        if not self.config.hmac_enabled:
            raise ValueError("HMAC is not enabled")

        expected_signature = self.generate_hmac(data)
        return hmac.compare_digest(expected_signature, signature)

    def generate_token(
        self,
        payload: Dict[str, Any],
        expiration: Optional[int] = None,
        security_level: SecurityLevel = SecurityLevel.MEDIUM
    ) -> str:
        """Generate a secure JWT-like token"""
        expiration = expiration or self.config.token_expiration
        expires_at = datetime.utcnow() + timedelta(seconds=expiration)

        # Create header
        header = {
            "alg": "HS256",
            "typ": "JWT",
            "sec": security_level.name
        }

        # Create payload
        token_payload = {
            **payload,
            "exp": expires_at.timestamp(),
            "iat": datetime.utcnow().timestamp(),
            "nbf": datetime.utcnow().timestamp()
        }

        # Encode header and payload
        header_b64 = self._base64url_encode(json.dumps(header).encode())
        payload_b64 = self._base64url_encode(json.dumps(token_payload).encode())

        # Create signature
        message = f"{header_b64}.{payload_b64}"
        signature = self._generate_signature(message)

        return f"{message}.{signature}"

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a token"""
        try:
            # Split token parts
            header_b64, payload_b64, signature = token.split('.')

            # Verify signature
            message = f"{header_b64}.{payload_b64}"
            if not self._verify_signature(message, signature):
                raise ValueError("Invalid token signature")

            # Decode payload
            payload = json.loads(self._base64url_decode(payload_b64))

            # Check expiration
            if datetime.utcnow().timestamp() > payload.get("exp", 0):
                raise ValueError("Token has expired")

            return payload

        except Exception as e:
            logging.error(f"Token verification failed: {e}")
            raise ValueError("Invalid token")

    def _generate_signature(self, message: str) -> str:
        """Generate HMAC signature for a message"""
        return hmac.new(
            self.config.token_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

    def _verify_signature(self, message: str, signature: str) -> bool:
        """Verify HMAC signature"""
        expected_signature = self._generate_signature(message)
        return hmac.compare_digest(expected_signature, signature)

    def _base64url_encode(self, data: bytes) -> str:
        """Base64 URL-safe encoding"""
        return base64.urlsafe_b64encode(data).decode().rstrip('=')

    def _base64url_decode(self, data: str) -> bytes:
        """Base64 URL-safe decoding"""
        # Add padding if needed
        padding = 4 - (len(data) % 4)
        if padding != 4:
            data += '=' * padding
        return base64.urlsafe_b64decode(data.encode())

    def generate_api_key(
        self,
        service_name: str,
        security_level: SecurityLevel = SecurityLevel.MEDIUM
    ) -> str:
        """Generate a secure API key"""
        # Generate random key
        random_key = secrets.token_hex(32)

        # Create key with prefix
        prefix = f"{service_name[:3].upper()}_{security_level.name[:3]}"
        api_key = f"{prefix}_{random_key}"

        # Store in config
        self.config.api_keys[api_key] = security_level

        return api_key

    def verify_api_key(self, api_key: str) -> SecurityLevel:
        """Verify API key and return security level"""
        if api_key not in self.config.api_keys:
            raise ValueError("Invalid API key")

        return self.config.api_keys[api_key]

    def check_ip_allowlist(self, ip_address: str) -> bool:
        """Check if IP address is allowed"""
        return ip_address in self.config.allowed_ips

    def check_rate_limit(self, operation: str, client_id: str) -> bool:
        """Check rate limit for an operation"""
        # This would be implemented with a proper rate limiting system
        # For now, just return True
        return True

    def generate_rsa_keys(self) -> Dict[str, str]:
        """Generate RSA key pair for asymmetric encryption"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        return {
            "private_key": private_pem,
            "public_key": public_pem
        }

    def rsa_encrypt(self, data: Union[str, bytes], public_key_pem: str) -> str:
        """Encrypt data using RSA public key"""
        if isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = data

        public_key = serialization.load_pem_public_key(
            public_key_pem.encode(),
            backend=default_backend()
        )

        encrypted = public_key.encrypt(
            data_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return base64.b64encode(encrypted).decode()

    def rsa_decrypt(self, encrypted_data: str, private_key_pem: str) -> bytes:
        """Decrypt data using RSA private key"""
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
            backend=default_backend()
        )

        encrypted_bytes = base64.b64decode(encrypted_data.encode())

        decrypted = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted

    def secure_hash(self, data: Union[str, bytes], salt: Optional[bytes] = None) -> str:
        """Generate secure hash with salt"""
        if isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = data

        if not salt:
            salt = secrets.token_bytes(16)

        # Use PBKDF2 for secure hashing
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        hash_value = kdf.derive(data_bytes)
        return f"{base64.b64encode(salt).decode()}${base64.b64encode(hash_value).decode()}"

    def verify_hash(self, data: Union[str, bytes], stored_hash: str) -> bool:
        """Verify secure hash"""
        if isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = data

        try:
            salt_b64, hash_b64 = stored_hash.split('$')
            salt = base64.b64decode(salt_b64.encode())
            stored_hash_value = base64.b64decode(hash_b64.encode())

            # Generate new hash with same salt
            new_hash = self.secure_hash(data, salt)

            # Compare
            return hmac.compare_digest(stored_hash, new_hash)

        except Exception:
            return False

    def secure_component_communication(
        self,
        message: Dict[str, Any],
        source_component: str,
        target_component: str
    ) -> Dict[str, Any]:
        """Secure communication between components"""
        # Generate timestamp
        timestamp = datetime.utcnow().isoformat()

        # Create secure message
        secure_message = {
            "source": source_component,
            "target": target_component,
            "timestamp": timestamp,
            "payload": message
        }

        # Encrypt payload
        if self.config.encryption_enabled:
            secure_message["encrypted_payload"] = self.encrypt_data(message)
            secure_message["payload"] = "[ENCRYPTED]"

        # Add HMAC
        if self.config.hmac_enabled:
            message_str = json.dumps(secure_message)
            secure_message["hmac"] = self.generate_hmac(message_str)

        return secure_message

    def verify_component_message(
        self,
        secure_message: Dict[str, Any],
        expected_source: Optional[str] = None,
        expected_target: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verify and decrypt component message"""
        # Verify HMAC first
        if self.config.hmac_enabled:
            message_str = json.dumps({
                k: v for k, v in secure_message.items()
                if k != "hmac"
            })
            if not self.verify_hmac(message_str, secure_message["hmac"]):
                raise ValueError("Invalid HMAC - message may have been tampered with")

        # Verify source and target
        if expected_source and secure_message.get("source") != expected_source:
            raise ValueError(f"Unexpected source: {secure_message.get('source')}")

        if expected_target and secure_message.get("target") != expected_target:
            raise ValueError(f"Unexpected target: {secure_message.get('target')}")

        # Decrypt payload if needed
        if "encrypted_payload" in secure_message:
            decrypted_payload = self.decrypt_data(secure_message["encrypted_payload"])
            secure_message["payload"] = decrypted_payload

        return secure_message["payload"]

# Example usage
if __name__ == "__main__":
    # Initialize security system
    security = SecuritySystem()

    # Test encryption
    test_data = {"message": "Hello, secure world!", "timestamp": datetime.utcnow().isoformat()}
    encrypted = security.encrypt_data(test_data)
    decrypted = security.decrypt_data(encrypted)
    print(f"Encryption test: {test_data == decrypted}")

    # Test token generation
    token = security.generate_token({"user_id": "123", "role": "admin"})
    print(f"Generated token: {token}")
    verified_payload = security.verify_token(token)
    print(f"Token verification: {verified_payload}")

    # Test API key
    api_key = security.generate_api_key("test_service", SecurityLevel.HIGH)
    print(f"Generated API key: {api_key}")
    security_level = security.verify_api_key(api_key)
    print(f"API key security level: {security_level}")

    # Test secure communication
    message = {"command": "process_data", "data": [1, 2, 3]}
    secure_message = security.secure_component_communication(message, "agent1", "agent2")
    print(f"Secure message: {secure_message}")
    verified_message = security.verify_component_message(secure_message, expected_source="agent1", expected_target="agent2")
    print(f"Verified message: {verified_message}")








