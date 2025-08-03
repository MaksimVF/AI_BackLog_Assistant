













"""
Team Management API Routes for AI Backlog Assistant - Test Version
"""

from flask import Blueprint, request, jsonify, g
from .team_billing_manager import TeamBillingManager
from .billing_manager import BillingException

team_test_bp = Blueprint('team_test', __name__)

@team_test_bp.route('/api/v1/team/members', methods=['POST'])
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

@team_test_bp.route('/api/v1/team/members', methods=['DELETE'])
def remove_team_member():
    """Remove a team member from the organization."""
    # For testing, use query parameters
    org_id = request.args.get('org_id', None)
    if not org_id:
        return jsonify({"error": "Organization ID is required"}), 400

    try:
        TeamBillingManager.remove_team_member(org_id)
        return jsonify({"message": "Team member removed successfully"})
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@team_test_bp.route('/api/v1/team/info', methods=['GET'])
def get_team_info():
    """Get information about the team."""
    # For testing, use query parameters
    org_id = request.args.get('org_id', None)
    if not org_id:
        return jsonify({"error": "Organization ID is required"}), 400

    try:
        team_info = TeamBillingManager.get_team_info(org_id)
        return jsonify(team_info)
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@team_test_bp.route('/api/v1/team/upgrade', methods=['POST'])
def upgrade_team_tariff():
    """Upgrade the organization to a new team tariff."""
    # For testing, use query parameters
    org_id = request.args.get('org_id', None)
    if not org_id:
        return jsonify({"error": "Organization ID is required"}), 400

    data = request.json
    new_tariff_id = data.get('tariff_id')

    if not new_tariff_id:
        return jsonify({"error": "Tariff ID is required"}), 400

    try:
        TeamBillingManager.upgrade_team_tariff(org_id, new_tariff_id)
        return jsonify({"message": "Team tariff upgraded successfully"})
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code


