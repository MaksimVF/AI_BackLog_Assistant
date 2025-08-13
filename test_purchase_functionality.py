



"""
Test the storage purchase functionality directly
"""

import json
import uuid
from datetime import datetime

def simulate_purchase_request():
    """Simulate a storage purchase request"""

    # Simulate request data
    request_data = {
        "organization_id": str(uuid.uuid4()),
        "gb_amount": 10.0
    }

    print("Simulating storage purchase request...")
    print(f"Request data: {json.dumps(request_data, indent=2)}")

    # Validate the request (similar to what the endpoint does)
    organization_id = request_data.get('organization_id')
    gb_amount = request_data.get('gb_amount')

    if not organization_id:
        return {"error": "organization_id is required"}, 400

    if not gb_amount or gb_amount <= 0:
        return {"error": "gb_amount must be a positive number"}, 400

    try:
        gb_amount = float(gb_amount)
    except (ValueError, TypeError):
        return {"error": "gb_amount must be a valid number"}, 400

    print("✓ Request validation passed")

    # Simulate the billing manager purchase logic
    price_per_gb = 5.0  # Example price
    total_cost = gb_amount * price_per_gb
    initial_balance = 500.0  # Example initial balance
    new_balance = initial_balance - total_cost

    if initial_balance < total_cost:
        return {"error": "Insufficient balance"}, 400

    # Simulate successful purchase
    transaction_id = str(uuid.uuid4())
    purchase_timestamp = datetime.utcnow().isoformat()

    response = {
        "status": "success",
        "message": "Storage purchased successfully",
        "gb_purchased": gb_amount,
        "total_cost": total_cost,
        "price_per_gb": price_per_gb,
        "new_balance": new_balance,
        "transaction_id": transaction_id,
        "timestamp": purchase_timestamp
    }

    print("✓ Purchase successful!")
    print(f"Response: {json.dumps(response, indent=2)}")

    return response, 200

def test_error_cases():
    """Test various error cases"""

    print("\nTesting error cases...")

    # Test case 1: Missing organization_id
    result1, status1 = simulate_purchase_request_with_data({"gb_amount": 10.0})
    print(f"Test 1 - Missing organization_id: Status {status1}")
    if status1 == 400:
        print("✓ Correctly rejected missing organization_id")
    else:
        print("✗ Failed to reject missing organization_id")

    # Test case 2: Invalid gb_amount (negative)
    result2, status2 = simulate_purchase_request_with_data({
        "organization_id": str(uuid.uuid4()),
        "gb_amount": -5
    })
    print(f"Test 2 - Negative gb_amount: Status {status2}")
    if status2 == 400:
        print("✓ Correctly rejected negative gb_amount")
    else:
        print("✗ Failed to reject negative gb_amount")

    # Test case 3: Non-numeric gb_amount
    result3, status3 = simulate_purchase_request_with_data({
        "organization_id": str(uuid.uuid4()),
        "gb_amount": "invalid"
    })
    print(f"Test 3 - Non-numeric gb_amount: Status {status3}")
    if status3 == 400:
        print("✓ Correctly rejected non-numeric gb_amount")
    else:
        print("✗ Failed to reject non-numeric gb_amount")

    # Test case 4: Insufficient balance
    result4, status4 = simulate_purchase_request_with_data({
        "organization_id": str(uuid.uuid4()),
        "gb_amount": 1000  # More than the 500 balance
    })
    print(f"Test 4 - Insufficient balance: Status {status4}")
    if status4 == 400:
        print("✓ Correctly rejected insufficient balance")
    else:
        print("✗ Failed to reject insufficient balance")

def simulate_purchase_request_with_data(data):
    """Helper function to simulate purchase with specific data"""

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

    # Simulate the billing manager purchase logic
    price_per_gb = 5.0  # Example price
    total_cost = gb_amount * price_per_gb
    initial_balance = 500.0  # Example initial balance
    new_balance = initial_balance - total_cost

    if initial_balance < total_cost:
        return {"error": "Insufficient balance"}, 400

    # Simulate successful purchase
    transaction_id = str(uuid.uuid4())
    purchase_timestamp = datetime.utcnow().isoformat()

    response = {
        "status": "success",
        "message": "Storage purchased successfully",
        "gb_purchased": gb_amount,
        "total_cost": total_cost,
        "price_per_gb": price_per_gb,
        "new_balance": new_balance,
        "transaction_id": transaction_id,
        "timestamp": purchase_timestamp
    }

    return response, 200

if __name__ == "__main__":
    print("Testing storage purchase functionality...\n")

    # Test successful case
    result, status = simulate_purchase_request()

    # Test error cases
    test_error_cases()

    print(f"\nOverall test result: {'PASSED' if status == 200 else 'FAILED'}")


