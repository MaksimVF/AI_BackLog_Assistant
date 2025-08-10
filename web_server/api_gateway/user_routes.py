




"""
User Management Routes for API Gateway
"""

import uuid
from flask import request, jsonify, current_app
from .gateway import api_gateway_bp
from .auth_middleware import token_required, generate_token
from ..app import db
from ..models import User, Organization, OrganizationMember, Document, DocumentAnalysis
from datetime import datetime


@api_gateway_bp.route('/api/v1/users', methods=['GET'])
@token_required
def get_users(current_user, current_email, current_role):
    """
    Get list of users (admin only)
    """
    if current_role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    # Get users with pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    users = User.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        } for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    })

@api_gateway_bp.route('/api/v1/users/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, current_email, current_role, user_id):
    """
    Get user details
    """
    # Allow users to get their own info, or admins to get any user
    if current_role != 'admin' and current_user != user_id:
        return jsonify({'error': 'Access denied'}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat()
    })

@api_gateway_bp.route('/api/v1/users', methods=['POST'])
def create_user():
    """
    Create a new user
    """
    data = request.get_json()

    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    username = data['username']
    email = data['email']
    password = data['password']

    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'error': 'Email already exists'}), 400

    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'user_id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    })

@api_gateway_bp.route('/api/v1/users/<user_id>', methods=['PUT'])
@token_required
def update_user(current_user, current_email, current_role, user_id):
    """
    Update user information
    """
    # Allow users to update their own info, or admins to update any user
    if current_role != 'admin' and current_user != user_id:
        return jsonify({'error': 'Access denied'}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    try:
        if 'username' in data:
            # Check if username is already taken
            existing_user = User.query.filter(User.username == data['username'], User.id != user_id).first()
            if existing_user:
                return jsonify({'error': 'Username already taken'}), 400
            user.username = data['username']

        if 'email' in data:
            # Check if email is already taken
            existing_email = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing_email:
                return jsonify({'error': 'Email already taken'}), 400
            user.email = data['email']

        if 'password' in data:
            user.set_password(data['password'])

        if 'is_active' in data and current_role == 'admin':
            user.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            'status': 'success',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active
        })

    except Exception as e:
        current_app.logger.error(f"User update error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'User update failed: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/users/<user_id>/documents', methods=['GET'])
@token_required
def get_user_documents(current_user, current_email, current_role, user_id):
    """
    Get user's documents (admin or self access only)
    """
    if current_role != 'admin' and current_user != user_id:
        return jsonify({'error': 'Access denied'}), 403

    # Get documents with pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', None)

    query = Document.query.filter_by(user_id=user_id)

    if status:
        query = query.filter(Document.status == status)

    documents = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'documents': [{
            'id': doc.id,
            'filename': doc.filename,
            'file_type': doc.file_type,
            'status': doc.status,
            'created_at': doc.created_at.isoformat(),
            'updated_at': doc.updated_at.isoformat() if doc.updated_at else None
        } for doc in documents.items],
        'total': documents.total,
        'pages': documents.pages,
        'current_page': documents.page
    })

@api_gateway_bp.route('/api/v1/users/<user_id>/analyses', methods=['GET'])
@token_required
def get_user_analyses(current_user, current_email, current_role, user_id):
    """
    Get user's analyses (admin or self access only)
    """
    if current_role != 'admin' and current_user != user_id:
        return jsonify({'error': 'Access denied'}), 403

    # Get analyses with pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    analysis_type = request.args.get('analysis_type', None)
    status = request.args.get('status', None)

    query = DocumentAnalysis.query.join(Document).filter(Document.user_id == user_id)

    if analysis_type:
        query = query.filter(DocumentAnalysis.analysis_type == analysis_type)

    if status:
        query = query.filter(DocumentAnalysis.status == status)

    analyses = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'analyses': [{
            'id': analysis.id,
            'document_id': analysis.document_id,
            'analysis_type': analysis.analysis_type,
            'status': analysis.status,
            'created_at': analysis.created_at.isoformat(),
            'updated_at': analysis.updated_at.isoformat() if analysis.updated_at else None
        } for analysis in analyses.items],
        'total': analyses.total,
        'pages': analyses.pages,
        'current_page': analyses.page
    })



