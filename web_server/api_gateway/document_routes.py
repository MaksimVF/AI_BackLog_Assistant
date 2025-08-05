



"""
Document Processing Routes for API Gateway
"""

import os
import tempfile
from flask import request, jsonify, current_app
from . import api_gateway_bp
from .auth_middleware import token_required
from ..app import db
from web_server.models import Document, DocumentAnalysis
from datetime import datetime

@api_gateway_bp.route('/api/v1/documents', methods=['GET', 'POST'])
@token_required
def handle_documents(current_user, current_email, current_role):
    """
    Handle document operations
    """
    if request.method == 'POST':
        # Upload and process a document
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        document_type = request.form.get('type', 'unknown')

        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        # Save the file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)

        try:
            # Process the document - for now use placeholder
            extracted_text = "Extracted text from document"
            metadata = {'pages': 5, 'format': document_type, 'size': '2.3MB'}

            # Create document record in database
            new_document = Document(
                user_id=current_user,
                filename=file.filename,
                file_type=document_type,
                status='processed',
                extracted_text=extracted_text,
                file_metadata=metadata
            )
            db.session.add(new_document)
            db.session.commit()

            # Clean up temp file
            os.remove(temp_path)

            return jsonify({
                'status': 'success',
                'message': 'Document uploaded and processed successfully',
                'document_id': new_document.id,
                'document_type': document_type,
                'user_id': current_user
            })

        except Exception as e:
            current_app.logger.error(f"Document processing error: {str(e)}")
            # Clean up temp file in case of error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({'error': f'Document processing failed: {str(e)}'}), 500

    else:
        # List documents for the user
        documents = Document.query.filter_by(user_id=current_user).all()

        return jsonify({
            'documents': [{
                'document_id': doc.id,
                'name': doc.filename,
                'status': doc.status,
                'uploaded_at': doc.created_at.isoformat() if doc.created_at else None,
                'file_type': doc.file_type
            } for doc in documents],
            'user_id': current_user
        })

@api_gateway_bp.route('/api/v1/documents/<document_id>', methods=['GET'])
@token_required
def get_document(current_user, current_email, current_role, document_id):
    """
    Get document processing status and results
    """
    document = Document.query.filter_by(id=document_id, user_id=current_user).first()

    if not document:
        return jsonify({'error': 'Document not found or access denied'}), 404

    return jsonify({
        'document_id': document.id,
        'status': document.status,
        'user_id': current_user,
        'filename': document.filename,
        'file_type': document.file_type,
        'metadata': document.file_metadata,
        'created_at': document.created_at.isoformat() if document.created_at else None,
        'updated_at': document.updated_at.isoformat() if document.updated_at else None
    })

@api_gateway_bp.route('/api/v1/documents/<document_id>/analysis', methods=['POST'])
@token_required
def analyze_document(current_user, current_email, current_role, document_id):
    """
    Request analysis of a processed document
    """
    document = Document.query.filter_by(id=document_id, user_id=current_user).first()

    if not document:
        return jsonify({'error': 'Document not found or access denied'}), 404

    data = request.get_json()
    analysis_type = data.get('analysis_type', 'basic')

    try:
        # Create analysis record
        analysis = DocumentAnalysis(
            document_id=document.id,
            analysis_type=analysis_type,
            status='processing',
            results={}
        )
        db.session.add(analysis)
        db.session.commit()

        # Update document status
        document.status = 'analyzed'
        document.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'status': 'analysis_started',
            'document_id': document.id,
            'analysis_id': analysis.id,
            'analysis_type': analysis_type,
            'user_id': current_user
        })

    except Exception as e:
        current_app.logger.error(f"Document analysis error: {str(e)}")
        return jsonify({'error': f'Document analysis failed: {str(e)}'}), 500


