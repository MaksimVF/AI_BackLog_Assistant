"""
API Gateway Module for AI Backlog Assistant
"""

from .gateway import api_gateway_bp

# Import routes to register them with the blueprint
from . import auth_routes
from . import document_routes
from . import analysis_routes
from . import user_routes
from . import organization_routes
from . import storage_routes
