

"""
Admin Panel Routes for AI Backlog Assistant
"""

import json
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g
from flask_login import login_required, current_user
from .extensions import db
from .models import User
from config.llm_config import (
    get_llm_config, set_llm_config, add_model_config, remove_model_config,
    set_default_model, LLMModelConfig, LLMProvider
)
from .billing_models import TariffPlan, OrganizationBalance, UsageLog
from .billing_manager import BillingManager

admin_bp = Blueprint('admin', __name__)

def require_admin_role():
    """Decorator to require admin role"""
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('index'))

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    require_admin_role()

    # Get LLM models
    llm_config = get_llm_config()
    llm_models = llm_config.models

    # Get tariff plans
    tariff_plans = TariffPlan.query.all()

    # Get recent transactions (usage logs)
    transactions = UsageLog.query.order_by(UsageLog.timestamp.desc()).limit(10).all()

    return render_template('admin.html',
                         llm_models=llm_models,
                         tariff_plans=tariff_plans,
                         transactions=transactions)

@admin_bp.route('/admin/llm', methods=['POST'])
@login_required
def manage_llm():
    """Manage LLM providers and models"""
    require_admin_role()

    action = request.form.get('action')

    try:
        if action == 'add_edit_model':
            # Add or edit LLM model
            model_name = request.form.get('model_name')
            provider = request.form.get('provider')
            api_key = request.form.get('api_key') or None
            api_url = request.form.get('api_url') or None
            max_tokens = int(request.form.get('max_tokens', 4096))
            temperature = float(request.form.get('temperature', 0.7))
            is_default = 'is_default' in request.form

            # Validate temperature
            if not 0 <= temperature <= 1:
                flash('Temperature must be between 0 and 1', 'error')
                return redirect(url_for('admin.admin_dashboard'))

            # Create model config
            model_config = LLMModelConfig(
                name=model_name,
                provider=LLMProvider(provider),
                api_key=api_key,
                api_url=api_url,
                max_tokens=max_tokens,
                temperature=temperature,
                is_default=is_default
            )

            # Add or update model
            add_model_config(model_config)

            # Set as default if requested
            if is_default:
                set_default_model(model_name)

            flash('LLM model saved successfully', 'success')

        elif action == 'delete_model':
            # Delete LLM model
            model_name = request.form.get('model_name')
            remove_model_config(model_name)
            flash('LLM model deleted successfully', 'success')

        elif action == 'set_default':
            # Set default model
            model_name = request.form.get('model_name')
            set_default_model(model_name)
            flash('Default model updated successfully', 'success')

        else:
            flash('Invalid action', 'error')

    except Exception as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/tariffs', methods=['POST'])
@login_required
def manage_tariffs():
    """Manage tariff plans"""
    require_admin_role()

    action = request.form.get('action')

    try:
        if action == 'add_edit_plan':
            # Add or edit tariff plan
            plan_name = request.form.get('plan_name')
            price_per_month = float(request.form.get('price_per_month'))
            included_limits = request.form.get('included_limits', '{}')
            discounts = request.form.get('discounts', '{}')
            access_features = request.form.get('access_features', '')

            # Parse JSON fields
            try:
                included_limits = json.loads(included_limits) if included_limits else {}
                discounts = json.loads(discounts) if discounts else {}
            except json.JSONDecodeError:
                flash('Invalid JSON format for limits or discounts', 'error')
                return redirect(url_for('admin.admin_dashboard'))

            # Parse access features
            access_features_list = [f.strip() for f in access_features.split(',')] if access_features else []

            # Check if plan exists
            existing_plan = TariffPlan.query.filter_by(name=plan_name).first()

            if existing_plan:
                # Update existing plan
                existing_plan.price_per_month = price_per_month
                existing_plan.included_limits = included_limits
                existing_plan.discounts = discounts
                existing_plan.access_features = access_features_list
                db.session.commit()
                flash('Tariff plan updated successfully', 'success')
            else:
                # Create new plan
                new_plan = TariffPlan(
                    name=plan_name,
                    price_per_month=price_per_month,
                    included_limits=included_limits,
                    discounts=discounts,
                    access_features=access_features_list
                )
                db.session.add(new_plan)
                db.session.commit()
                flash('Tariff plan created successfully', 'success')

        elif action == 'delete_plan':
            # Delete tariff plan
            plan_id = request.form.get('plan_id')
            plan = TariffPlan.query.get(plan_id)

            if plan:
                # Check if any organizations are using this plan
                orgs_using_plan = OrganizationBalance.query.filter_by(tariff_plan_id=plan_id).count()
                if orgs_using_plan > 0:
                    flash('Cannot delete plan - organizations are using it', 'error')
                else:
                    db.session.delete(plan)
                    db.session.commit()
                    flash('Tariff plan deleted successfully', 'success')
            else:
                flash('Plan not found', 'error')

        else:
            flash('Invalid action', 'error')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/payments', methods=['POST'])
@login_required
def manage_payments():
    """Manage payments and transactions"""
    require_admin_role()

    action = request.form.get('action')

    try:
        if action == 'manual_transaction':
            # Add manual transaction
            organization_id = request.form.get('organization_id')
            amount = float(request.form.get('amount'))
            description = request.form.get('description', 'Manual transaction')

            # Add funds to organization
            try:
                new_balance = BillingManager.top_up(organization_id, amount)

                # Log the transaction
                transaction = UsageLog(
                    organization_id=organization_id,
                    feature="manual_transaction",
                    units_used=1,
                    price_charged=amount,
                    additional_data={
                        "description": description,
                        "transaction_type": "manual",
                        "amount": amount
                    }
                )
                db.session.add(transaction)
                db.session.commit()

                flash(f'Added {amount} RUB to organization {organization_id}', 'success')
            except Exception as e:
                flash(f'Failed to add funds: {str(e)}', 'error')

        else:
            flash('Invalid action', 'error')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/api/llm', methods=['GET', 'POST', 'DELETE'])
@login_required
def admin_llm_api():
    """Admin API for LLM management"""
    require_admin_role()

    if request.method == 'GET':
        # Return current LLM configuration
        llm_config = get_llm_config()

        # Convert to dict for JSON serialization
        config_dict = {
            "default_provider": llm_config.default_provider.value,
            "models": [{
                "name": model.name,
                "provider": model.provider.value,
                "max_tokens": model.max_tokens,
                "temperature": model.temperature,
                "is_default": model.is_default
            } for model in llm_config.models]
        }

        return jsonify(config_dict)

    elif request.method == 'POST':
        # Add or update model
        data = request.get_json()

        try:
            model_config = LLMModelConfig(
                name=data['name'],
                provider=LLMProvider(data['provider']),
                api_key=data.get('api_key'),
                api_url=data.get('api_url'),
                max_tokens=data.get('max_tokens', 4096),
                temperature=data.get('temperature', 0.7),
                is_default=data.get('is_default', False)
            )

            add_model_config(model_config)

            if data.get('is_default', False):
                set_default_model(data['name'])

            return jsonify({"status": "success", "message": "Model updated"})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    elif request.method == 'DELETE':
        # Delete model
        data = request.get_json()
        model_name = data.get('model_name')

        if model_name:
            remove_model_config(model_name)
            return jsonify({"status": "success", "message": "Model deleted"})

        return jsonify({"status": "error", "message": "Model name required"}), 400

@admin_bp.route('/admin/api/tariffs', methods=['GET', 'POST', 'DELETE'])
@login_required
def admin_tariffs_api():
    """Admin API for tariff management"""
    require_admin_role()

    if request.method == 'GET':
        # Return all tariff plans
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

    elif request.method == 'POST':
        # Add or update tariff plan
        data = request.get_json()

        try:
            plan_id = data.get('id')
            if plan_id:
                # Update existing plan
                plan = TariffPlan.query.get(plan_id)
                if not plan:
                    return jsonify({"status": "error", "message": "Plan not found"}), 404
            else:
                # Create new plan
                plan = TariffPlan()

            plan.name = data['name']
            plan.price_per_month = data['price_per_month']
            plan.included_limits = data.get('included_limits', {})
            plan.discounts = data.get('discounts', {})
            plan.access_features = data.get('access_features', [])

            if not plan_id:
                db.session.add(plan)

            db.session.commit()

            return jsonify({"status": "success", "message": "Plan saved"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 400

    elif request.method == 'DELETE':
        # Delete tariff plan
        data = request.get_json()
        plan_id = data.get('id')

        if plan_id:
            plan = TariffPlan.query.get(plan_id)
            if plan:
                # Check if any organizations are using this plan
                orgs_using_plan = OrganizationBalance.query.filter_by(tariff_plan_id=plan_id).count()
                if orgs_using_plan > 0:
                    return jsonify({"status": "error", "message": "Cannot delete - plan in use"}), 400

                db.session.delete(plan)
                db.session.commit()
                return jsonify({"status": "success", "message": "Plan deleted"})

            return jsonify({"status": "error", "message": "Plan not found"}), 404

        return jsonify({"status": "error", "message": "Plan ID required"}), 400

