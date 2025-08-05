





"""
Organization Management Routes for API Gateway
"""

from flask import request, jsonify
from . import api_gateway_bp
from .auth_middleware import token_required


from ..app import db
from ..models import Organization, OrganizationMember, User



@api_gateway_bp.route('/api/v1/organizations', methods=['POST'])
@token_required
def create_organization(current_user, current_email, current_role):
    """
    Create a new organization
    """
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Organization name is required'}), 400

    name = data['name']

    # Create new organization
    new_org = Organization(name=name, created_by=current_user)
    db.session.add(new_org)
    db.session.commit()

    # Add the creator as the owner
    membership = OrganizationMember(
        user_id=current_user,
        organization_id=new_org.id,
        role='owner'
    )
    db.session.add(membership)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'organization_id': new_org.id,
        'name': new_org.name,
        'created_by': current_user
    })

@api_gateway_bp.route('/api/v1/organizations', methods=['GET'])
@token_required
def get_organizations(current_user, current_email, current_role):
    """
    Get list of organizations for the current user
    """
    # Get organizations where user is a member
    memberships = OrganizationMember.query.filter_by(user_id=current_user).all()

    organizations = []
    for membership in memberships:
        org = Organization.query.get(membership.organization_id)
        if org:
            organizations.append({
                'id': org.id,
                'name': org.name,
                'role': membership.role,
                'created_at': org.created_at.isoformat()
            })

    return jsonify({'organizations': organizations})

@api_gateway_bp.route('/api/v1/organizations/<org_id>', methods=['GET'])
@token_required
def get_organization(current_user, current_email, current_role, org_id):
    """
    Get organization details
    """
    # Check if user is a member of the organization
    membership = OrganizationMember.query.filter_by(
        user_id=current_user,
        organization_id=org_id
    ).first()

    if not membership:
        return jsonify({'error': 'Access denied'}), 403

    org = Organization.query.get(org_id)

    if not org:
        return jsonify({'error': 'Organization not found'}), 404

    return jsonify({
        'id': org.id,
        'name': org.name,
        'created_by': org.created_by,
        'created_at': org.created_at.isoformat(),
        'current_user_role': membership.role
    })

@api_gateway_bp.route('/api/v1/organizations/<org_id>/members', methods=['GET'])
@token_required
def get_organization_members(current_user, current_email, current_role, org_id):
    """
    Get organization members
    """
    # Check if user has permission to view members
    membership = OrganizationMember.query.filter_by(
        user_id=current_user,
        organization_id=org_id
    ).first()

    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403

    # Get all members
    members = OrganizationMember.query.filter_by(organization_id=org_id).all()

    result = []
    for member in members:
        user = User.query.get(member.user_id)
        if user:
            result.append({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': member.role,
                'joined_at': member.joined_at.isoformat()
            })

    return jsonify({'members': result})

@api_gateway_bp.route('/api/v1/organizations/<org_id>/members', methods=['POST'])
@token_required
def add_organization_member(current_user, current_email, current_role, org_id):
    """
    Add a member to the organization
    """
    # Check if user has permission to add members
    membership = OrganizationMember.query.filter_by(
        user_id=current_user,
        organization_id=org_id
    ).first()

    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()

    if not data or 'user_id' not in data or 'role' not in data:
        return jsonify({'error': 'User ID and role are required'}), 400

    user_id = data['user_id']
    role = data['role']

    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if already a member
    existing_membership = OrganizationMember.query.filter_by(
        user_id=user_id,
        organization_id=org_id
    ).first()

    if existing_membership:
        return jsonify({'error': 'User already a member'}), 400

    # Add to organization
    new_membership = OrganizationMember(
        user_id=user_id,
        organization_id=org_id,
        role=role
    )
    db.session.add(new_membership)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'user_id': user_id,
        'role': role
    })




