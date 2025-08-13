

"""
Test script for BillingManager storage purchase functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_server')))

from web_server.billing_manager import BillingManager
from web_server.extensions import db
from web_server.billing_models import OrganizationBalance, TariffPlan
from web_server.models import User
import uuid
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

# Create a test Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_billing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test_secret'

# Initialize extensions
db.init_app(app)

def test_billing_manager():
    """Test the BillingManager storage purchase functionality"""

    with app.app_context():
        # Create database
        db.create_all()

        # Create test data
        test_org_id = str(uuid.uuid4())

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

        print("Test data created successfully")
        print(f"Organization ID: {test_org_id}")
        print(f"Initial balance: {org_balance.balance_rub}")

        # Test storage purchase
        try:
            # Test successful purchase
            result = BillingManager.purchase_storage(
                organization_id=test_org_id,
                gb_amount=10.0
            )

            print("Purchase successful!")
            print(f"GB purchased: {result['gb_purchased']}")
            print(f"Total cost: {result['total_cost']}")
            print(f"Price per GB: {result['price_per_gb']}")
            print(f"New balance: {result['new_balance']}")
            print(f"Transaction ID: {result['transaction_id']}")

            # Check that balance was deducted correctly
            updated_balance = OrganizationBalance.query.filter_by(organization_id=test_org_id).first()
            print(f"Database balance: {updated_balance.balance_rub}")

            # Test insufficient balance
            try:
                result2 = BillingManager.purchase_storage(
                    organization_id=test_org_id,
                    gb_amount=100.0  # This should fail
                )
                print("ERROR: Purchase with insufficient balance succeeded!")
            except Exception as e:
                print(f"Expected error for insufficient balance: {str(e)}")

        except Exception as e:
            print("Error during purchase:", str(e))
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_billing_manager()

