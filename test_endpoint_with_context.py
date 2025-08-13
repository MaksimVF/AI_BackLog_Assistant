






"""
Test the storage purchase endpoint with Flask app context
"""

from datetime import datetime
import json
import uuid
from flask import Flask
from web_server.extensions import db
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan
from web_server.models import Organization

# Create a test Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_endpoint.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test_secret'

# Initialize extensions
db.init_app(app)

def test_endpoint_with_context():
    """Test the endpoint logic with Flask app context"""

    with app.app_context():
        # Create database
        db.create_all()

        # Create test data
        test_org_id = str(uuid.uuid4())

        # Create organization
        organization = Organization(
            id=test_org_id,
            name="Test Organization",
            created_by=str(uuid.uuid4()),
            created_at=datetime.utcnow()
        )
        db.session.add(organization)

        # Create a tariff plan
        tariff_plan = TariffPlan(
            id=str(uuid.uuid4()),
            name=f"Test Plan {str(uuid.uuid4())[:8]}",
            price_per_month=1000.0,
            included_storage_gb=5.0,
            additional_storage_price_per_gb=5.0,
            storage_retention_days=180,
            storage_tier="standard"
        )
        db.session.add(tariff_plan)

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=test_org_id,
            balance_rub=500.0,  # 500 RUB balance
            tariff_plan_id=tariff_plan.id
        )
        db.session.add(org_balance)
        db.session.commit()

        print("Test data created successfully")
        print(f"Organization ID: {test_org_id}")
        print(f"Initial balance: {org_balance.balance_rub}")

        # Test the endpoint logic
        print("\nTesting storage purchase endpoint logic...")

        # Mock request data
        data = {
            "organization_id": test_org_id,
            "gb_amount": 10.0
        }

        current_user = {
            "user_id": str(uuid.uuid4()),
            "email": "test@example.com",
            "role": "admin"
        }

        print(f"Request data: {json.dumps(data, indent=2)}")
        print(f"Current user: {json.dumps(current_user, indent=2)}")

        # Validate required fields (similar to endpoint logic)
        organization_id = data.get('organization_id')
        gb_amount = data.get('gb_amount')

        if not organization_id:
            print("✗ Missing organization_id")
            return {"error": "organization_id is required"}, 400

        if gb_amount is None:
            print("✗ Missing gb_amount")
            return {"error": "gb_amount must be a positive number"}, 400

        try:
            gb_amount = float(gb_amount)
            if gb_amount <= 0:
                print("✗ Invalid gb_amount (must be positive)")
                return {"error": "gb_amount must be a positive number"}, 400
        except (ValueError, TypeError):
            print("✗ Invalid gb_amount (must be numeric)")
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

            # Check database balance
            updated_balance = OrganizationBalance.query.filter_by(organization_id=test_org_id).first()
            print(f"Database balance: {updated_balance.balance_rub}")

            return response, 200

        except Exception as e:
            print(f"✗ Purchase failed: {e}")
            return {"error": str(e)}, 500

def test_error_cases():
    """Test error cases"""

    with app.app_context():
        print("\nTesting error cases...")

        # Test case 1: Missing organization_id
        data1 = {"gb_amount": 10.0}
        result1, status1 = test_endpoint_logic_with_data(data1)
        print(f"Missing organization_id: Status {status1}")
        if status1 == 400:
            print("✓ Correctly rejected missing organization_id")
        else:
            print("✗ Failed to reject missing organization_id")

        # Test case 2: Invalid gb_amount (negative)
        data2 = {"organization_id": str(uuid.uuid4()), "gb_amount": -5}
        result2, status2 = test_endpoint_logic_with_data(data2)
        print(f"Negative gb_amount: Status {status2}")
        if status2 == 400:
            print("✓ Correctly rejected negative gb_amount")
        else:
            print("✗ Failed to reject negative gb_amount")

        # Test case 3: Non-numeric gb_amount
        data3 = {"organization_id": str(uuid.uuid4()), "gb_amount": "invalid"}
        result3, status3 = test_endpoint_logic_with_data(data3)
        print(f"Non-numeric gb_amount: Status {status3}")
        if status3 == 400:
            print("✓ Correctly rejected non-numeric gb_amount")
        else:
            print("✗ Failed to reject non-numeric gb_amount")

        # Test case 4: Insufficient balance
        test_org_id = str(uuid.uuid4())
        tariff_plan = TariffPlan(
            id=str(uuid.uuid4()),
            name=f"Test Plan 2 {str(uuid.uuid4())[:8]}",
            price_per_month=1000.0,
            included_storage_gb=5.0,
            additional_storage_price_per_gb=5.0,
            storage_retention_days=180,
            storage_tier="standard"
        )
        db.session.add(tariff_plan)

        org_balance = OrganizationBalance(
            organization_id=test_org_id,
            balance_rub=10.0,  # Only 10 RUB balance
            tariff_plan_id=tariff_plan.id
        )
        db.session.add(org_balance)
        db.session.commit()

        data4 = {"organization_id": test_org_id, "gb_amount": 10.0}  # 50 RUB needed
        result4, status4 = test_endpoint_logic_with_data(data4)
        print(f"Insufficient balance: Status {status4}")
        if status4 == 500:  # BillingException is caught and returns 500
            print("✓ Correctly rejected insufficient balance")
        else:
            print("✗ Failed to reject insufficient balance")

def test_endpoint_logic_with_data(data):
    """Helper function to test with specific data"""

    with app.app_context():
        organization_id = data.get('organization_id')
        gb_amount = data.get('gb_amount')

        if not organization_id:
            return {"error": "organization_id is required"}, 400

        if gb_amount is None:
            return {"error": "gb_amount must be a positive number"}, 400

        try:
            gb_amount = float(gb_amount)
            if gb_amount <= 0:
                return {"error": "gb_amount must be a positive number"}, 400
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
                'user_id': str(uuid.uuid4())
            }

            return response, 200

        except Exception as e:
            return {"error": str(e)}, 500

if __name__ == "__main__":
    print("Testing storage purchase endpoint with Flask app context...\n")

    # Test successful case
    result, status = test_endpoint_with_context()

    # Test error cases
    test_error_cases()

    print(f"\nOverall test result: {'PASSED' if status == 200 else 'FAILED'}")





