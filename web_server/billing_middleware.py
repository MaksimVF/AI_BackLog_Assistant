


"""
Billing Middleware for AI Backlog Assistant

Provides decorators and middleware for integrating billing checks into agent calls.
"""

from functools import wraps
from flask import g, request, jsonify
from .billing_manager import BillingManager, BillingException

def billing_required(feature_name: str, units: int = 1):
    """
    Decorator to protect agent calls with billing checks.

    Args:
        feature_name: The name of the feature being used
        units: Number of units to charge (default: 1)

    Returns:
        decorator function
    """
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            # Check if there's a current organization
            if not g.organization:
                return jsonify({"error": "No organization selected"}), 400

            try:
                # Charge for the feature usage
                amount_charged = BillingManager.charge(
                    organization_id=g.organization.id,
                    feature_name=feature_name,
                    units=units,
                    user_id=getattr(g, 'user_id', None)
                )

                # Add billing info to request context
                g.billing_info = {
                    "feature": feature_name,
                    "units": units,
                    "amount_charged": amount_charged
                }

                # Call the original function
                return f(*args, **kwargs)

            except BillingException as e:
                return jsonify({"error": str(e)}), e.status_code
            except Exception as e:
                return jsonify({"error": f"Billing error: {str(e)}"}), 500

        return wrapped_function
    return decorator

def get_billing_info():
    """
    Get billing information from the current request context.

    Returns:
        dict: Billing information
    """
    return getattr(g, 'billing_info', {})

