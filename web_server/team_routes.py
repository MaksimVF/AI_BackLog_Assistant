












"""
Team Management API Routes for AI Backlog Assistant
"""

from flask import Blueprint, request, jsonify, g
from flask_login import login_required, current_user
from .team_billing_manager import TeamBillingManager
from .billing_manager import BillingException

team_bp = Blueprint('team', __name__)

@team_bp.route('/api/v1/team/members', methods=['POST'])
def add_team_member():
    """Add a new team member to the organization."""
    # For testing, use query parameters
    org_id = request.args.get('org_id', None)
    if not org_id:
        return jsonify({"error": "Organization ID is required"}), 400

    try:
        TeamBillingManager.add_team_member(org_id)
        return jsonify({"message": "Team member added successfully"})
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@team_bp.route('/api/v1/team/members', methods=['DELETE'])
@login_required
def remove_team_member():
    """Remove a team member from the organization."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    try:
        TeamBillingManager.remove_team_member(g.organization.id)
        return jsonify({"message": "Team member removed successfully"})
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@team_bp.route('/api/v1/team/info', methods=['GET'])
@login_required
def get_team_info():
    """Get information about the team."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    try:
        team_info = TeamBillingManager.get_team_info(g.organization.id)
        return jsonify(team_info)
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@team_bp.route('/api/v1/team/upgrade', methods=['POST'])
@login_required
def upgrade_team_tariff():
    """Upgrade the organization to a new team tariff."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    data = request.json
    new_tariff_id = data.get('tariff_id')

    if not new_tariff_id:
        return jsonify({"error": "Tariff ID is required"}), 400

    try:
        TeamBillingManager.upgrade_team_tariff(g.organization.id, new_tariff_id)
        return jsonify({"message": "Team tariff upgraded successfully"})
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

