

"""
Organization Management Routes for API Gateway
"""

import uuid
from flask import request, jsonify, current_app
from . import api_gateway_bp
from .auth_middleware import token_required
from ..app import db
from ..models import Organization, OrganizationMember, User, Document, DocumentAnalysis
from datetime import datetime

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

    try:
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

    except Exception as e:
        current_app.logger.error(f"Organization creation error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Organization creation failed: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/organizations', methods=['GET'])
@token_required
def get_organizations(current_user, current_email, current_role):
    """
    Get list of organizations for the current user
    """
    try:
        # Get organizations where user is a member
        memberships = OrganizationMember.query.filter_by(user_id=current_user).all()

        organizations = []
        for membership in memberships:
            org = Organization.query.get(membership.organization_id)
            if org:
                # Get document and analysis counts for this organization
                doc_count = Document.query.filter_by(organization_id=org.id).count()
                analysis_count = DocumentAnalysis.query.join(Document).filter(Document.organization_id == org.id).count()

                organizations.append({
                    'id': org.id,
                    'name': org.name,
                    'role': membership.role,
                    'created_at': org.created_at.isoformat(),
                    'document_count': doc_count,
                    'analysis_count': analysis_count,
                    'member_count': OrganizationMember.query.filter_by(organization_id=org.id).count()
                })

        return jsonify({'organizations': organizations})

    except Exception as e:
        current_app.logger.error(f"Get organizations error: {str(e)}")
        return jsonify({'error': f'Failed to retrieve organizations: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/organizations/<org_id>', methods=['GET'])
@token_required
def get_organization(current_user, current_email, current_role, org_id):
    """
    Get organization details
    """
    try:
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

        # Get document statistics
        doc_count = Document.query.filter_by(organization_id=org.id).count()
        analysis_count = DocumentAnalysis.query.join(Document).filter(Document.organization_id == org.id).count()

        # Get recent documents
        recent_documents = Document.query.filter_by(organization_id=org.id).order_by(Document.created_at.desc()).limit(5).all()

        return jsonify({
            'id': org.id,
            'name': org.name,
            'created_by': org.created_by,
            'created_at': org.created_at.isoformat(),
            'current_user_role': membership.role,
            'document_count': doc_count,
            'analysis_count': analysis_count,
            'member_count': OrganizationMember.query.filter_by(organization_id=org.id).count(),
            'recent_documents': [{
                'id': doc.id,
                'filename': doc.filename,
                'status': doc.status,
                'created_at': doc.created_at.isoformat()
            } for doc in recent_documents]
        })

    except Exception as e:
        current_app.logger.error(f"Get organization error: {str(e)}")
        return jsonify({'error': f'Failed to retrieve organization: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/organizations/<org_id>/members', methods=['GET'])
@token_required
def get_organization_members(current_user, current_email, current_role, org_id):
    """
    Get organization members
    """
    try:
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
                # Get document and analysis counts for this member in this organization
                doc_count = Document.query.filter_by(user_id=user.id, organization_id=org_id).count()
                analysis_count = DocumentAnalysis.query.join(Document).filter(
                    Document.user_id == user.id,
                    Document.organization_id == org_id
                ).count()

                result.append({
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': member.role,
                    'joined_at': member.joined_at.isoformat(),
                    'document_count': doc_count,
                    'analysis_count': analysis_count
                })

        return jsonify({'members': result})

    except Exception as e:
        current_app.logger.error(f"Get organization members error: {str(e)}")
        return jsonify({'error': f'Failed to retrieve members: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/organizations/<org_id>/members', methods=['POST'])
@token_required
def add_organization_member(current_user, current_email, current_role, org_id):
    """
    Add a member to the organization
    """
    try:
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

    except Exception as e:
        current_app.logger.error(f"Add organization member error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Failed to add member: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/organizations/<org_id>/documents', methods=['GET'])
@token_required
def get_organization_documents(current_user, current_email, current_role, org_id):
    """
    Get organization documents
    """
    try:
        # Check if user is a member of the organization
        membership = OrganizationMember.query.filter_by(
            user_id=current_user,
            organization_id=org_id
        ).first()

        if not membership:
            return jsonify({'error': 'Access denied'}), 403

        # Get documents with pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None)
        user_id = request.args.get('user_id', None)

        query = Document.query.filter_by(organization_id=org_id)

        if status:
            query = query.filter(Document.status == status)

        if user_id:
            query = query.filter(Document.user_id == user_id)

        documents = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'documents': [{
                'id': doc.id,
                'filename': doc.filename,
                'file_type': doc.file_type,
                'status': doc.status,
                'user_id': doc.user_id,
                'created_at': doc.created_at.isoformat(),
                'updated_at': doc.updated_at.isoformat() if doc.updated_at else None
            } for doc in documents.items],
            'total': documents.total,
            'pages': documents.pages,
            'current_page': documents.page
        })

    except Exception as e:
        current_app.logger.error(f"Get organization documents error: {str(e)}")
        return jsonify({'error': f'Failed to retrieve documents: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/organizations/<org_id>/analyses', methods=['GET'])
@token_required
def get_organization_analyses(current_user, current_email, current_role, org_id):
    """
    Get organization analyses
    """
    try:
        # Check if user is a member of the organization
        membership = OrganizationMember.query.filter_by(
            user_id=current_user,
            organization_id=org_id
        ).first()

        if not membership:
            return jsonify({'error': 'Access denied'}), 403

        # Get analyses with pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        analysis_type = request.args.get('analysis_type', None)
        status = request.args.get('status', None)
        user_id = request.args.get('user_id', None)

        query = DocumentAnalysis.query.join(Document).filter(Document.organization_id == org_id)

        if analysis_type:
            query = query.filter(DocumentAnalysis.analysis_type == analysis_type)

        if status:
            query = query.filter(DocumentAnalysis.status == status)

        if user_id:
            query = query.filter(Document.user_id == user_id)

        analyses = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'analyses': [{
                'id': analysis.id,
                'document_id': analysis.document_id,
                'analysis_type': analysis.analysis_type,
                'status': analysis.status,
                'user_id': Document.query.get(analysis.document_id).user_id,
                'created_at': analysis.created_at.isoformat(),
                'updated_at': analysis.updated_at.isoformat() if analysis.updated_at else None
            } for analysis in analyses.items],
            'total': analyses.total,
            'pages': analyses.pages,
            'current_page': analyses.page
        })

    except Exception as e:
        current_app.logger.error(f"Get organization analyses error: {str(e)}")
        return jsonify({'error': f'Failed to retrieve analyses: {str(e)}'}), 500

