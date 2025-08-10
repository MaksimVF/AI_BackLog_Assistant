


"""
Authentication Routes for API Gateway
"""

from flask import request, jsonify
from .gateway import api_gateway_bp
from .auth_middleware import generate_token, token_required
from werkzeug.security import check_password_hash
from ..app import db
from ..models import User

@api_gateway_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token
    """
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    # Find user by email
    user = User.query.filter_by(email=email).first()

    if not user or not user.password_hash:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Check password
    if not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate access and refresh tokens
    access_token = generate_token(user.id, user.email, role='user', token_type='access')
    refresh_token = generate_token(user.id, user.email, role='user', token_type='refresh')

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': 3600  # 1 hour in seconds
    })

@api_gateway_bp.route('/api/v1/auth/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh access token using refresh token
    """
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'error': 'Refresh token is required'}), 400

    try:
        # Validate refresh token
        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if payload['type'] != 'refresh':
            return jsonify({'error': 'Invalid token type'}), 401

        # Generate new access token
        access_token = generate_token(payload['sub'], payload['email'], role=payload['role'], token_type='access')

        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 3600  # 1 hour in seconds
        })

    except ExpiredSignatureError:
        return jsonify({'error': 'Refresh token has expired'}), 401
    except InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token'}), 401

@api_gateway_bp.route('/api/v1/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user, current_email, current_role):
    """
    Get current authenticated user information
    """
    user = User.query.get(current_user)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': current_role,
        'is_active': user.is_active
    })

