

"""
JWT Authentication Middleware for API Gateway
"""

import os
import datetime
from functools import wraps
from flask import request, jsonify, current_app
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-jwt-secret-key-here')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_MINUTES = 60  # Token expires in 60 minutes
JWT_EXPIRE_DAYS = 30  # Refresh token expires in 30 days

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
    Decorator to require JWT authentication
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
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Decode token
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            current_user = data['sub']
            current_email = data['email']
            current_role = data['role']
        except ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401

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

