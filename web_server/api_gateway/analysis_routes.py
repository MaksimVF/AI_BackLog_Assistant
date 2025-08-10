


"""
Analysis Routes for API Gateway
"""

import json
from flask import request, jsonify, current_app
from .gateway import api_gateway_bp
from .auth_middleware import token_required
from ..app import db
from web_server.models import Document, DocumentAnalysis
from datetime import datetime
from agents.pipeline_coordinator_agent import PipelineCoordinatorAgent
from agents.analyzers.sentiment_analyzer import SentimentAnalyzer
from agents.analyzers.entity_extractor import EntityExtractor
from agents.summary.summary_agent import SummaryAgent

# Initialize agents
pipeline_coordinator = PipelineCoordinatorAgent()
sentiment_analyzer = SentimentAnalyzer()
entity_extractor = EntityExtractor()
summary_agent = SummaryAgent()

@api_gateway_bp.route('/api/v1/analysis', methods=['POST'])
@token_required
def create_analysis(current_user, current_email, current_role):
    """
    Create a new analysis request using real agents
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Text content is required for analysis'}), 400

    text = data['text']
    analysis_type = data.get('analysis_type', 'basic')
    document_id = data.get('document_id')

    try:
        # Create analysis record
        analysis = DocumentAnalysis(
            document_id=document_id,
            analysis_type=analysis_type,
            status='processing',
            results={}
        )
        db.session.add(analysis)
        db.session.commit()

        # Perform actual analysis using real agents
        results = {}
        if analysis_type == 'sentiment':
            # Use real sentiment analyzer
            sentiment_result = sentiment_analyzer.analyze(text)
            results['sentiment'] = sentiment_result.get('sentiment', 'neutral')
            results['confidence'] = sentiment_result.get('confidence', 0.7)
        elif analysis_type == 'entity':
            # Use real entity extractor
            entities = entity_extractor.extract(text)
            results['entities'] = [{'name': entity['text'], 'type': entity['type']} for entity in entities]
        elif analysis_type == 'summarization':
            # Use real summary agent
            summary = summary_agent.generate_summary(text)
            results['summary'] = summary
        elif analysis_type == 'categorization':
            # Use document classifier
            category = document_classifier.classify(text)
            results['categories'] = [category]
        else:  # basic - comprehensive analysis
            # Use pipeline coordinator for comprehensive analysis
            pipeline_result = pipeline_coordinator.process_document(text)
            results = {
                'sentiment': pipeline_result.get('sentiment', {}).get('sentiment', 'neutral'),
                'entities': pipeline_result.get('entities', []),
                'summary': pipeline_result.get('summary', {}).get('summary', 'No summary available'),
                'categories': pipeline_result.get('categories', [])
            }

        # Update analysis record with results
        analysis.status = 'completed'
        analysis.results = results
        analysis.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'status': 'analysis_completed',
            'analysis_id': analysis.id,
            'analysis_type': analysis_type,
            'user_id': current_user,
            'results': results
        })

    except Exception as e:
        current_app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/analysis/<analysis_id>', methods=['GET'])
@token_required
def get_analysis_results(current_user, current_email, current_role, analysis_id):
    """
    Get analysis results
    """
    analysis = DocumentAnalysis.query.get(analysis_id)

    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404

    # Check if user has access to this analysis
    document = Document.query.get(analysis.document_id)
    if not document or document.user_id != current_user:
        return jsonify({'error': 'Access denied'}), 403

    return jsonify({
        'analysis_id': analysis.id,
        'status': analysis.status,
        'analysis_type': analysis.analysis_type,
        'results': analysis.results,
        'created_at': analysis.created_at.isoformat() if analysis.created_at else None,
        'updated_at': analysis.updated_at.isoformat() if analysis.updated_at else None
    })

@api_gateway_bp.route('/api/v1/analysis/types', methods=['GET'])
@token_required
def get_analysis_types(current_user, current_email, current_role):
    """
    Get available analysis types
    """
    # Return available analysis types with more details
    return jsonify({
        'analysis_types': [
            {'name': 'basic', 'description': 'Comprehensive text analysis including sentiment, entities, and summarization'},
            {'name': 'sentiment', 'description': 'Detailed sentiment analysis of the text'},
            {'name': 'entity', 'description': 'Entity extraction and classification'},
            {'name': 'summarization', 'description': 'Automatic text summarization'},
            {'name': 'categorization', 'description': 'Document categorization and classification'}
        ]
    })

