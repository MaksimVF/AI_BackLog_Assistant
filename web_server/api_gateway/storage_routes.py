

"""
Storage Management Routes for API Gateway
"""

from flask import request, jsonify, current_app
from .gateway import api_gateway_bp
from .auth_middleware import token_required
from web_server.storage_manager import StorageManager, StorageException
from web_server.billing_manager import BillingManager, BillingException

@api_gateway_bp.route('/api/v1/storage/cleanup', methods=['POST'])
@token_required
def storage_cleanup(current_user, current_email, current_role):
    """
    Trigger storage cleanup for expired content.

    Expected JSON payload (optional):
    {
        "organization_id": "org_123"  # Optional: clean up for specific organization
    }
    """
    try:
        data = request.get_json() if request.is_json else {}
        organization_id = data.get('organization_id')

        try:
            if organization_id:
                # Clean up for specific organization
                # Get organization's tariff plan to determine retention
                org_balance = BillingManager.get_balance(organization_id)
                # Apply retention policy
                result = StorageManager.apply_retention_policy(
                    organization_id=organization_id,
                    retention_days=180  # Default retention, could be from tariff plan
                )
            else:
                # Global cleanup
                result = StorageManager.cleanup_expired_storage()

            return jsonify({
                'status': 'success',
                'message': 'Storage cleanup completed',
                'cleanup_report': result
            })

        except StorageException as e:
            return jsonify({'error': str(e), 'status_code': e.status_code}), e.status_code
        except Exception as e:
            current_app.logger.error(f"Storage cleanup error: {str(e)}")
            return jsonify({'error': f'Storage cleanup failed: {str(e)}'}), 500

    except Exception as e:
        current_app.logger.error(f"Storage cleanup error: {str(e)}")
        return jsonify({'error': f'Storage cleanup failed: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/storage/usage', methods=['GET'])
@token_required
def get_storage_usage(current_user, current_email, current_role):
    """
    Get storage usage statistics for an organization.

    Expected query parameters:
    - organization_id: The organization ID
    """
    try:
        organization_id = request.args.get('organization_id')
        if not organization_id:
            return jsonify({'error': 'organization_id is required'}), 400

        try:
            usage_result = StorageManager.get_storage_usage(
                organization_id=organization_id
            )

            return jsonify(usage_result)

        except StorageException as e:
            return jsonify({'error': str(e), 'status_code': e.status_code}), e.status_code
        except Exception as e:
            current_app.logger.error(f"Storage usage error: {str(e)}")
            return jsonify({'error': f'Storage usage calculation failed: {str(e)}'}), 500

    except Exception as e:
        current_app.logger.error(f"Storage usage error: {str(e)}")
        return jsonify({'error': f'Storage usage calculation failed: {str(e)}'}), 500

@api_gateway_bp.route('/api/v1/storage/quota', methods=['GET'])
@token_required
def check_storage_quota(current_user, current_email, current_role):
    """
    Check storage quota enforcement for an organization.

    Expected query parameters:
    - organization_id: The organization ID
    """
    try:
        organization_id = request.args.get('organization_id')
        if not organization_id:
            return jsonify({'error': 'organization_id is required'}), 400

        try:
            quota_result = StorageManager.enforce_storage_quotas(
                organization_id=organization_id
            )

            return jsonify(quota_result)

        except StorageException as e:
            return jsonify({'error': str(e), 'status_code': e.status_code}), e.status_code
        except Exception as e:
            current_app.logger.error(f"Storage quota error: {str(e)}")
            return jsonify({'error': f'Storage quota check failed: {str(e)}'}), 500

    except Exception as e:
        current_app.logger.error(f"Storage quota error: {str(e)}")
        return jsonify({'error': f'Storage quota check failed: {str(e)}'}), 500

