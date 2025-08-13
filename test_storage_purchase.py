
"""
Test script for storage purchase functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_server')))

from api_gateway.document_routes import purchase_storage
from flask import Flask
from extensions import db
from models import User
from billing_models import OrganizationBalance, TariffPlan
from billing_manager import BillingManager
import uuid

# Create a test Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test_secret'

# Initialize extensions
db.init_app(app)

def test_storage_purchase():
    """Test the storage purchase functionality"""

    with app.app_context():
        # Create database
        db.create_all()

        # Create test data
        test_org_id = str(uuid.uuid4())
        test_user_id = str(uuid.uuid4())

        # Create a tariff plan
        tariff_plan = TariffPlan(
            id=str(uuid.uuid4()),
            name="Test Plan",
            price_per_month=1000.0,
            included_storage_gb=5.0,
            additional_storage_price_per_gb=5.0,
            storage_retention_days=180,
            storage_tier="standard"
        )
        db.session.add(tariff_plan)
        db.session.commit()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=test_org_id,
            balance_rub=500.0,  # 500 RUB balance
            tariff_plan_id=tariff_plan.id
        )
        db.session.add(org_balance)
        db.session.commit()

        # Create test user
        test_user = User(
            id=test_user_id,
            username="testuser",
            email="test@example.com",
            password_hash="hashedpassword",
            role="user"
        )
        db.session.add(test_user)
        db.session.commit()

        print("Test data created successfully")
        print(f"Organization ID: {test_org_id}")
        print(f"User ID: {test_user_id}")
        print(f"Initial balance: {org_balance.balance_rub}")

        # Test storage purchase
        try:
            # Mock request data
            class MockRequest:
                def get_json(self):
                    return {
                        "organization_id": test_org_id,
                        "gb_amount": 10.0
                    }

            # Mock current user
            current_user = test_user_id
            current_email = "test@example.com"
            current_role = "user"

            # Call the purchase function
            result = purchase_storage(
                current_user=current_user,
                current_email=current_email,
                current_role=current_role
            )

            print("Purchase result:", result)

        except Exception as e:
            print("Error during purchase:", str(e))
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_storage_purchase()
