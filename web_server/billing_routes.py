


"""
Billing API Routes for AI Backlog Assistant
"""

from flask import Blueprint, request, jsonify, g
from flask_login import login_required, current_user
from .billing_manager import BillingManager, BillingException
from .billing_models import OrganizationBalance, UsageLog, TariffPlan, FeatureConfig
from .app import db

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/api/v1/billing/balance', methods=['GET'])
@login_required
def get_balance():
    """Get current organization balance."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    try:
        balance = BillingManager.get_balance(g.organization.id)
        return jsonify({
            "organization_id": g.organization.id,
            "balance_rub": balance,
            "currency": "RUB"
        })
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@billing_bp.route('/api/v1/billing/usage', methods=['GET'])
@login_required
def get_usage():
    """Get usage history for the organization."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    feature = request.args.get('feature')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Parse dates if provided
    start_dt = None
    end_dt = None
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400

    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400

    try:
        usage_logs = BillingManager.get_usage_history(
            g.organization.id,
            feature_name=feature,
            start_date=start_dt,
            end_date=end_dt
        )

        return jsonify({
            "organization_id": g.organization.id,
            "usage": [{
                "id": log.id,
                "feature": log.feature,
                "units_used": log.units_used,
                "price_charged": log.price_charged,
                "timestamp": log.timestamp.isoformat()
            } for log in usage_logs]
        })
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@billing_bp.route('/api/v1/billing/limits', methods=['GET'])
@login_required
def get_limits():
    """Get current limits and usage for the organization."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    try:
        org_balance = OrganizationBalance.query.filter_by(organization_id=g.organization.id).first()
        if not org_balance or not org_balance.tariff_plan_id:
            return jsonify({
                "organization_id": g.organization.id,
                "tariff_plan": "None",
                "limits": {}
            })

        tariff_plan = TariffPlan.query.get(org_balance.tariff_plan_id)
        if not tariff_plan:
            return jsonify({
                "organization_id": g.organization.id,
                "tariff_plan": "None",
                "limits": {}
            })

        limits = tariff_plan.included_limits or {}
        result = {
            "organization_id": g.organization.id,
            "tariff_plan": tariff_plan.name,
            "limits": {}
        }

        for feature, total_limit in limits.items():
            remaining, total = BillingManager.check_limit(g.organization.id, feature)
            result["limits"][feature] = {
                "total": total,
                "remaining": remaining,
                "used": total - remaining
            }

        return jsonify(result)

    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@billing_bp.route('/api/v1/billing/topup', methods=['POST'])
@login_required
def top_up_balance():
    """Add funds to organization balance."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "Amount is required"}), 400

    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400

        new_balance = BillingManager.top_up(g.organization.id, amount)

        return jsonify({
            "organization_id": g.organization.id,
            "new_balance": new_balance,
            "amount_added": amount
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount format"}), 400
    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

@billing_bp.route('/api/v1/billing/features', methods=['GET'])
@login_required
def get_available_features():
    """Get features available for the organization's tariff plan."""
    if not g.organization:
        return jsonify({"error": "No organization selected"}), 400

    try:
        org_balance = OrganizationBalance.query.filter_by(organization_id=g.organization.id).first()
        if not org_balance or not org_balance.tariff_plan_id:
            return jsonify({
                "organization_id": g.organization.id,
                "tariff_plan": "None",
                "features": []
            })

        tariff_plan = TariffPlan.query.get(org_balance.tariff_plan_id)
        if not tariff_plan:
            return jsonify({
                "organization_id": g.organization.id,
                "tariff_plan": "None",
                "features": []
            })

        features = BillingManager.get_tariff_features(tariff_plan.id)

        # Get feature details
        feature_configs = FeatureConfig.query.filter(FeatureConfig.feature_name.in_(features)).all()
        feature_details = [{
            "name": config.feature_name,
            "type": config.feature_type,
            "price_per_unit": config.price_per_unit,
            "description": config.description
        } for config in feature_configs]

        return jsonify({
            "organization_id": g.organization.id,
            "tariff_plan": tariff_plan.name,
            "features": feature_details
        })

    except BillingException as e:
        return jsonify({"error": str(e)}), e.status_code

# Admin routes (for demonstration purposes, should be protected in production)
@billing_bp.route('/api/v1/admin/billing/tariffs', methods=['GET'])
def get_tariff_plans():
    """Get all tariff plans (admin)."""
    tariffs = TariffPlan.query.all()
    return jsonify({
        "tariffs": [{
            "id": t.id,
            "name": t.name,
            "price_per_month": t.price_per_month,
            "included_limits": t.included_limits,
            "discounts": t.discounts,
            "access_features": t.access_features
        } for t in tariffs]
    })

@billing_bp.route('/api/v1/admin/billing/features', methods=['GET'])
def get_feature_configs():
    """Get all feature configurations (admin)."""
    features = FeatureConfig.query.all()
    return jsonify({
        "features": [{
            "name": f.feature_name,
            "type": f.feature_type,
            "unit": f.unit,
            "price_per_unit": f.price_per_unit,
            "access_tariffs": f.access_tariffs,
            "description": f.description
        } for f in features]
    })

