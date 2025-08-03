


#!/usr/bin/env python3

"""
Simple Billing System Test
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan

def test_simple_billing():
    """Test basic billing functionality."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Organization",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Get the Free tariff plan
        tariff_plan = TariffPlan.query.filter_by(name="Free").first()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=100.0,  # Add some balance
            tariff_plan_id=tariff_plan.id if tariff_plan else None
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Test 1: Check initial balance
        balance = BillingManager.get_balance(org_id)
        print(f"Initial balance: {balance} RUB")

        # Test 2: Check limits
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"CategorizationAgent limits: {remaining}/{total} calls")

        # Test 3: Charge for usage
        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=1,
                user_id="test-user-id"
            )
            print(f"Charged {amount_charged} RUB for CategorizationAgent usage")

            # Check balance after usage
            new_balance = BillingManager.get_balance(org_id)
            print(f"Balance after usage: {new_balance} RUB")

            # Check remaining limits
            remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
            print(f"Remaining limits: {remaining}/{total} calls")

        except Exception as e:
            print(f"Error during charging: {e}")

if __name__ == "__main__":
    test_simple_billing()


