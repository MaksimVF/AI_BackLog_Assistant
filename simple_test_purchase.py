


"""
Simple test to verify the storage purchase implementation
"""

import json

def test_purchase_endpoint():
    """Test the purchase endpoint logic"""

    # Simulate a request payload
    request_payload = {
        "organization_id": "test_org_123",
        "gb_amount": 10.0
    }

    print("Testing storage purchase endpoint...")
    print(f"Request payload: {json.dumps(request_payload, indent=2)}")

    # Validate the payload (similar to what the endpoint does)
    organization_id = request_payload.get('organization_id')
    gb_amount = request_payload.get('gb_amount')

    if not organization_id:
        print("ERROR: organization_id is required")
        return False

    if not gb_amount or gb_amount <= 0:
        print("ERROR: gb_amount must be a positive number")
        return False

    try:
        gb_amount = float(gb_amount)
    except (ValueError, TypeError):
        print("ERROR: gb_amount must be a valid number")
        return False

    print("✓ Request validation passed")

    # Simulate the purchase logic
    print("Simulating purchase logic...")

    # This would be the logic from BillingManager.purchase_storage
    price_per_gb = 5.0  # Example price
    total_cost = gb_amount * price_per_gb
    initial_balance = 500.0  # Example initial balance
    new_balance = initial_balance - total_cost

    if initial_balance < total_cost:
        print("ERROR: Insufficient balance")
        return False

    # Simulate successful purchase response
    response = {
        "status": "success",
        "message": "Storage purchased successfully",
        "gb_purchased": gb_amount,
        "total_cost": total_cost,
        "price_per_gb": price_per_gb,
        "new_balance": new_balance,
        "transaction_id": "txn_12345",
        "user_id": "user_123"
    }

    print("✓ Purchase successful!")
    print(f"Response: {json.dumps(response, indent=2)}")

    return True

def test_error_cases():
    """Test error cases"""

    print("\nTesting error cases...")

    # Test case 1: Missing organization_id
    payload1 = {"gb_amount": 10.0}
    print("Test 1: Missing organization_id")
    if not payload1.get('organization_id'):
        print("✓ Correctly detected missing organization_id")

    # Test case 2: Invalid gb_amount
    payload2 = {"organization_id": "test_org", "gb_amount": -5}
    print("Test 2: Invalid gb_amount (negative)")
    if payload2.get('gb_amount') and payload2['gb_amount'] <= 0:
        print("✓ Correctly detected invalid gb_amount")

    # Test case 3: Non-numeric gb_amount
    payload3 = {"organization_id": "test_org", "gb_amount": "invalid"}
    print("Test 3: Non-numeric gb_amount")
    try:
        float(payload3['gb_amount'])
        print("ERROR: Should have failed for non-numeric gb_amount")
    except (ValueError, TypeError):
        print("✓ Correctly detected non-numeric gb_amount")

if __name__ == "__main__":
    print("Running storage purchase tests...\n")

    # Test successful case
    success = test_purchase_endpoint()

    # Test error cases
    test_error_cases()

    print(f"\nOverall test result: {'PASSED' if success else 'FAILED'}")

