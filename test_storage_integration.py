

"""
Test script for storage integration functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'web_server')))

from flask import Flask
from extensions import db
from models import User, Organization
from billing_models import OrganizationBalance, TariffPlan, StoragePricing
from billing_manager import BillingManager
from storage_manager import StorageManager
import uuid

# Create a test Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_storage_integration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test_secret'

# Initialize extensions
db.init_app(app)

def test_storage_integration():
    """Test the storage integration functionality"""

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

        # Create organization
        organization = Organization(
            id=test_org_id,
            name="Test Organization"
        )
        db.session.add(organization)
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
            role="user",
            organization_id=test_org_id,
            storage_quota_mb=2048,  # 2GB
            storage_tier="standard"
        )
        db.session.add(test_user)
        db.session.commit()

        print("Test data created successfully")
        print(f"Organization ID: {test_org_id}")
        print(f"User ID: {test_user_id}")

        # Test storage cost calculation
        try:
            cost_result = BillingManager.calculate_storage_costs(test_org_id)
            print("Storage cost calculation result:", cost_result)
        except Exception as e:
            print("Storage cost calculation error:", str(e))

        # Test storage usage
        try:
            usage_result = StorageManager.get_storage_usage(test_org_id)
            print("Storage usage result:", usage_result)
        except Exception as e:
            print("Storage usage error:", str(e))

        # Test storage quota enforcement
        try:
            quota_result = StorageManager.enforce_storage_quotas(test_org_id)
            print("Storage quota result:", quota_result)
        except Exception as e:
            print("Storage quota error:", str(e))

        # Test storage purchase
        try:
            purchase_result = BillingManager.purchase_storage(
                organization_id=test_org_id,
                gb_amount=1.0
            )
            print("Storage purchase result:", purchase_result)
        except Exception as e:
            print("Storage purchase error:", str(e))

if __name__ == "__main__":
    test_storage_integration()

