




"""
Security Improvements

Critical security fixes and enhancements for the AI BackLog Assistant.
"""

import os
import re
import subprocess
from typing import Dict, Any, Optional
import logging
from functools import wraps

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_audit.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('security_improvements')

class SecurityConfig:
    """Security configuration and utilities"""

    @staticmethod
    def get_secure_config() -> Dict[str, Any]:
        """Get secure configuration with defaults"""
        return {
            'MAX_INPUT_LENGTH': 10000,
            'ALLOWED_FILE_EXTENSIONS': ['.pdf', '.txt', '.docx', '.xlsx'],
            'RATE_LIMIT': '100/hour',
            'JWT_EXPIRATION': 3600,  # 1 hour
            'PASSWORD_MIN_LENGTH': 12,
            'SECRET_KEY_LENGTH': 32
        }

    @staticmethod
    def validate_input(text: str, max_length: int = 10000) -> bool:
        """Validate user input"""
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
    def sanitize_path(file_path: str, allowed_extensions: Optional[list] = None) -> str:
        """Sanitize file paths to prevent traversal"""
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
    def secure_subprocess(command: list, input_data: Optional[str] = None) -> str:
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

def secure_api_endpoint(func):
    """Decorator for securing API endpoints"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Input validation
        for arg in args:
            if isinstance(arg, str) and not SecurityConfig.validate_input(arg):
                logger.warning("Invalid input detected")
                raise ValueError("Invalid input")

        # Rate limiting (simulated)
        # In production, use a proper rate limiting library
        # rate_limiter.check()

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API endpoint error: {str(e)}")
            raise

    return wrapper

def remove_hardcoded_secrets():
    """Remove hardcoded secrets from codebase"""
    secret_patterns = [
        (r'password\s*=\s*["\'].*["\']', 'password'),
        (r'secret\s*=\s*["\'].*["\']', 'secret'),
        (r'api_key\s*=\s*["\'].*["\']', 'api_key'),
        (r'token\s*=\s*["\'].*["\']', 'token')
    ]

    files_checked = 0
    secrets_found = 0

    for root, dirs, files in os.walk('.'):
        # Skip test and virtual environments
        if any(skip in root for skip in ['__pycache__', '.git', 'node_modules', 'test_', 'benchmark']):
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for secrets
                    for pattern, secret_type in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            secrets_found += 1
                            logger.warning(f"Hardcoded {secret_type} found in: {file_path}")

                    files_checked += 1

                except Exception as e:
                    logger.error(f"Error checking {file_path}: {str(e)}")

    logger.info(f"Checked {files_checked} files, found {secrets_found} potential secrets")
    return secrets_found

def implement_secure_config():
    """Implement secure configuration"""
    config = SecurityConfig.get_secure_config()

    # Save to secure config file
    with open('secure_config.json', 'w') as f:
        import json
        json.dump(config, f, indent=2)

    logger.info("Secure configuration implemented")
    return config

def main():
    """Main security improvements function"""
    print("Implementing security improvements...")

    # 1. Remove hardcoded secrets
    print("\n1. Scanning for hardcoded secrets...")
    secrets_found = remove_hardcoded_secrets()

    # 2. Implement secure configuration
    print("\n2. Implementing secure configuration...")
    config = implement_secure_config()

    # 3. Test input validation
    print("\n3. Testing input validation...")
    test_inputs = [
        "Valid input text",
        "SELECT * FROM users; -- SQL injection attempt",
        "A" * 20000,  # Too long
        "Normal text with 'quotes' and \\backslashes"
    ]

    for i, test_input in enumerate(test_inputs, 1):
        is_valid = SecurityConfig.validate_input(test_input)
        print(f"   Test {i}: {'✓' if is_valid else '✗'} - {test_input[:50]}...")

    # 4. Test path sanitization
    print("\n4. Testing path sanitization...")
    test_paths = [
        "safe_file.txt",
        "../../malicious.py",
        "/etc/passwd",
        "valid.pdf",
        "document.docx"
    ]

    for i, test_path in enumerate(test_paths, 1):
        try:
            sanitized = SecurityConfig.sanitize_path(
                test_path,
                allowed_extensions=['.txt', '.pdf', '.docx']
            )
            print(f"   Test {i}: ✓ - {test_path} -> {sanitized}")
        except ValueError as e:
            print(f"   Test {i}: ✗ - {test_path} - {str(e)}")

    print("\nSecurity improvements completed!")
    print(f"Summary: {secrets_found} potential secrets found, secure config implemented")

if __name__ == "__main__":
    main()




