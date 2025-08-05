
"""
API Gateway Module for AI Backlog Assistant
"""

from flask import Blueprint

# Create API Gateway Blueprint
api_gateway_bp = Blueprint('api_gateway', __name__)

# Import routes to register them with the blueprint
from . import auth_routes
from . import document_routes
from . import analysis_routes
from . import user_routes
from . import organization_routes
