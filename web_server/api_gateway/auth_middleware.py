

"""
Enhanced JWT Authentication Middleware with improved security and validation for API Gateway
"""

import os
import datetime
import logging
from functools import wraps
from flask import request, jsonify, current_app, g, after_this_request
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from security.api_security import verify_jwt_token, generate_hmac_signature
from utils.error_handling import SecurityError

# Configure logging
logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-jwt-secret-key-here')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_MINUTES = 60  # Token expires in 60 minutes

JWT_EXPIRE_DAYS = 30  # Refresh token expires in 30 days

# Security headers
SECURE_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'; frame-ancestors 'none'"
}


def generate_token(user_id, email, role='user', token_type='access'):
    """
    Generate JWT token
    """
    if token_type == 'access':
        expire_delta = datetime.timedelta(minutes=JWT_EXPIRE_MINUTES)
    else:  # refresh token
        expire_delta = datetime.timedelta(days=JWT_EXPIRE_DAYS)

    payload = {
        'sub': user_id,
        'email': email,
        'role': role,
        'type': token_type,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + expire_delta
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def token_required(f):
    """
    Enhanced decorator to require JWT authentication with additional security checks
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            logger.warning("Authentication attempt without token")
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Verify token using enhanced security
            payload = verify_jwt_token(token)
            current_user = payload['sub']
            current_email = payload['email']
            current_role = payload['role']

            # Log successful authentication
            logger.info(f"User {current_user} ({current_email}) authenticated successfully")

            # Add security headers to response
            @after_this_request
            def add_security_headers(response):
                for header, value in SECURE_HEADERS.items():
                    response.headers[header] = value
                return response

        except ExpiredSignatureError:
            logger.warning("Expired token detected")
            return jsonify({'error': 'Token has expired'}), 401
        except InvalidTokenError:
            logger.warning("Invalid token detected")
            return jsonify({'error': 'Token is invalid'}), 401
        except SecurityError as e:
            logger.warning(f"Security error: {str(e)}")
            return jsonify({'error': str(e)}), 401

        return f(current_user, current_email, current_role, *args, **kwargs)

    return decorated

def validate_token(token):
    """
    Validate JWT token and return payload if valid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return None  # Token expired
    except InvalidTokenError:
        return None  # Invalid token

