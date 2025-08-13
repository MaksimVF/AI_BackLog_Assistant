





"""
Test the storage purchase endpoint logic without Flask app
"""

import json
import uuid
from datetime import datetime
from web_server.billing_manager import BillingManager

def mock_request_data():
    """Create mock request data"""
    return {
        "organization_id": str(uuid.uuid4()),
        "gb_amount": 10.0
    }

def mock_current_user():
    """Create mock current user data"""
    return {
        "user_id": str(uuid.uuid4()),
        "email": "test@example.com",
        "role": "admin"
    }

def test_endpoint_logic():
    """Test the endpoint logic without Flask"""

    print("Testing storage purchase endpoint logic...")

    # Mock request data
    data = mock_request_data()
    current_user = mock_current_user()

    print(f"Request data: {json.dumps(data, indent=2)}")
    print(f"Current user: {json.dumps(current_user, indent=2)}")

    # Validate required fields (similar to endpoint logic)
    organization_id = data.get('organization_id')
    gb_amount = data.get('gb_amount')

    if not organization_id:
        return {"error": "organization_id is required"}, 400

    if not gb_amount or gb_amount <= 0:
        return {"error": "gb_amount must be a positive number"}, 400

    try:
        gb_amount = float(gb_amount)
    except (ValueError, TypeError):
        return {"error": "gb_amount must be a valid number"}, 400

    print("✓ Request validation passed")

    # Call the billing manager (same as endpoint)
    try:
        purchase_result = BillingManager.purchase_storage(
            organization_id=organization_id,
            gb_amount=gb_amount
        )

        # Format response (same as endpoint)
        response = {
            'status': 'success',
            'message': 'Storage purchased successfully',
            'gb_purchased': purchase_result['gb_purchased'],
            'total_cost': purchase_result['total_cost'],
            'price_per_gb': purchase_result['price_per_gb'],
            'new_balance': purchase_result['new_balance'],
            'transaction_id': purchase_result['transaction_id'],
            'user_id': current_user['user_id']
        }

        print("✓ Purchase successful!")
        print(f"Response: {json.dumps(response, indent=2)}")

        return response, 200

    except Exception as e:
        print(f"✗ Purchase failed: {e}")
        return {"error": str(e)}, 500

def test_error_cases():
    """Test error cases"""

    print("\nTesting error cases...")

    # Test missing organization_id
    data1 = {"gb_amount": 10.0}
    result1, status1 = test_endpoint_logic_with_data(data1)
    print(f"Missing organization_id: Status {status1}")
    if status1 == 400:
        print("✓ Correctly rejected missing organization_id")
    else:
        print("✗ Failed to reject missing organization_id")

    # Test invalid gb_amount
    data2 = {"organization_id": str(uuid.uuid4()), "gb_amount": -5}
    result2, status2 = test_endpoint_logic_with_data(data2)
    print(f"Negative gb_amount: Status {status2}")
    if status2 == 400:
        print("✓ Correctly rejected negative gb_amount")
    else:
        print("✗ Failed to reject negative gb_amount")

    # Test non-numeric gb_amount
    data3 = {"organization_id": str(uuid.uuid4()), "gb_amount": "invalid"}
    result3, status3 = test_endpoint_logic_with_data(data3)
    print(f"Non-numeric gb_amount: Status {status3}")
    if status3 == 400:
        print("✓ Correctly rejected non-numeric gb_amount")
    else:
        print("✗ Failed to reject non-numeric gb_amount")

def test_endpoint_logic_with_data(data):
    """Helper function to test with specific data"""

    current_user = mock_current_user()

    organization_id = data.get('organization_id')
    gb_amount = data.get('gb_amount')

    if not organization_id:
        return {"error": "organization_id is required"}, 400

    if not gb_amount or gb_amount <= 0:
        return {"error": "gb_amount must be a positive number"}, 400

    try:
        gb_amount = float(gb_amount)
    except (ValueError, TypeError):
        return {"error": "gb_amount must be a valid number"}, 400

    try:
        purchase_result = BillingManager.purchase_storage(
            organization_id=organization_id,
            gb_amount=gb_amount
        )

        response = {
            'status': 'success',
            'message': 'Storage purchased successfully',
            'gb_purchased': purchase_result['gb_purchased'],
            'total_cost': purchase_result['total_cost'],
            'price_per_gb': purchase_result['price_per_gb'],
            'new_balance': purchase_result['new_balance'],
            'transaction_id': purchase_result['transaction_id'],
            'user_id': current_user['user_id']
        }

        return response, 200

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    print("Testing storage purchase endpoint logic...\n")

    # Test successful case
    result, status = test_endpoint_logic()

    # Test error cases
    test_error_cases()

    print(f"\nOverall test result: {'PASSED' if status == 200 else 'FAILED'}")




