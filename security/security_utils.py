




"""
Security Utilities

Core security functions and utilities for the AI BackLog Assistant.
"""

import os
import re
import hashlib
import hmac
import secrets
import logging
from typing import Optional, Dict, Any, List
from functools import wraps
import subprocess

# Configure secure logging
logger = logging.getLogger('security_utils')

class SecurityUtils:
    """Core security utilities"""

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a cryptographically secure token"""
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_password(password: str) -> str:
        """Securely hash a password using bcrypt"""
        import bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against a bcrypt hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def validate_input(text: str, max_length: int = 10000) -> bool:
        """Validate user input for security"""
        if not text or len(text) > max_length:
            return False

        # Check for suspicious patterns
        suspicious_patterns = [
            r'[\'\";\\]',
            r'(\b(?:SELECT|INSERT|UPDATE|DELETE|DROP)\b)',
            r'(\b(?:OR\s+1=1|--|/\*|;\s*SHUTDOWN)\b)',
            r'(\b(?:exec|system|sp_|xp_)\b)',
            r'(\b(?:UNION\s+SELECT|WAITFOR\s+DELAY)\b)'
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False

        return True

    @staticmethod
    def sanitize_path(file_path: str, allowed_extensions: Optional[List[str]] = None) -> str:
        """Sanitize file paths to prevent traversal attacks"""
        if not file_path:
            raise ValueError("Empty file path")

        # Normalize path
        sanitized = os.path.normpath(file_path)

        # Check for traversal attempts
        if '..' in sanitized or sanitized.startswith('/'):
            raise ValueError("Invalid file path")

        # Check extension if provided
        if allowed_extensions:
            ext = os.path.splitext(sanitized)[1].lower()
            if ext not in allowed_extensions:
                raise ValueError(f"Invalid file extension: {ext}")

        return sanitized

    @staticmethod
    def secure_subprocess(command: List[str], input_data: Optional[str] = None) -> str:
        """Secure subprocess execution"""
        if not isinstance(command, list):
            raise ValueError("Command must be a list")

        try:
            result = subprocess.run(
                command,
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                shell=False  # Never use shell=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Subprocess error: {e.stderr}")
            raise

    @staticmethod
    def get_secure_config() -> Dict[str, Any]:
        """Get secure default configuration"""
        return {
            'MAX_INPUT_LENGTH': 10000,
            'ALLOWED_FILE_EXTENSIONS': ['.pdf', '.txt', '.docx', '.xlsx'],
            'RATE_LIMIT': '100/hour',
            'JWT_EXPIRATION': 3600,  # 1 hour
            'PASSWORD_MIN_LENGTH': 12,
            'SECRET_KEY_LENGTH': 32
        }

def secure_api_endpoint(func):
    """Decorator for securing API endpoints"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Input validation
        for arg in args:
            if isinstance(arg, str) and not SecurityUtils.validate_input(arg):
                logger.warning("Invalid input detected")
                raise ValueError("Invalid input")

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API endpoint error: {str(e)}")
            raise

    return wrapper

def check_environment_security():
    """Check environment for security issues"""
    issues = []

    # Check for debug mode
    if os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1', 'yes'):
        issues.append("Debug mode is enabled in production")

    # Check for missing security headers
    required_headers = ['X-Content-Type-Options', 'X-Frame-Options', 'Content-Security-Policy']
    # In a real implementation, we'd check the actual response headers

    # Check for weak permissions
    sensitive_files = ['secure_config.json', 'config.py', 'settings.py']
    for file in sensitive_files:
        if os.path.exists(file):
            try:
                st = os.stat(file)
                if st.st_mode & 0o007:  # World writable
                    issues.append(f"File {file} has weak permissions")
            except:
                pass

    return issues

def remove_sensitive_data_from_logs(data: str) -> str:
    """Remove sensitive data from logs"""
    patterns = [
        (r'password\s*=\s*["\'].*?["\']', 'password="[REDACTED]"'),
        (r'secret\s*=\s*["\'].*?["\']', 'secret="[REDACTED]"'),
        (r'api_key\s*=\s*["\'].*?["\']', 'api_key="[REDACTED]"'),
        (r'token\s*=\s*["\'].*?["\']', 'token="[REDACTED]"')
    ]

    for pattern, replacement in patterns:
        data = re.sub(pattern, replacement, data, flags=re.IGNORECASE)

    return data

# Initialize security
def init_security():
    """Initialize security utilities"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('security.log'),
            logging.StreamHandler()
        ]
    )

    # Check environment
    issues = check_environment_security()
    if issues:
        logger.warning(f"Security issues found: {issues}")

    logger.info("Security utilities initialized")

# Initialize on import
init_security()





