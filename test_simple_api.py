









#!/usr/bin/env python3

"""
Test Billing API Directly
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan
from web_server.billing_routes import billing_bp

def test_billing_api_direct():
    """Test billing API directly."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test API Direct",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Get the Free tariff plan
        tariff_plan = TariffPlan.query.filter_by(name="Free").first()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=5.0,
            tariff_plan_id=tariff_plan.id if tariff_plan else None
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Test the BillingManager methods directly
        print("\nTesting BillingManager methods:")

        # Test get_balance
        balance = BillingManager.get_balance(org_id)
        print(f"Balance: {balance} RUB")

        # Test check_limit
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Limits: {remaining}/{total}")

        # Test charge (within limits)
        amount_charged = BillingManager.charge(
            organization_id=org_id,
            feature_name="CategorizationAgent",
            units=1,
            user_id="test-user-id"
        )
        print(f"Charged for 1 unit: {amount_charged} RUB")

        # Check new balance and limits
        new_balance = BillingManager.get_balance(org_id)
        new_remaining, new_total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"New balance: {new_balance} RUB")
        print(f"New limits: {new_remaining}/{new_total}")

        # Test charge beyond limits
        for i in range(99):  # Use up remaining limits
            BillingManager.charge(org_id, "CategorizationAgent", 1, "test-user-id")

        # Check state
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"After using all limits - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Charge beyond limits
        amount_charged = BillingManager.charge(
            organization_id=org_id,
            feature_name="CategorizationAgent",
            units=1,
            user_id="test-user-id"
        )
        print(f"Charged beyond limits: {amount_charged} RUB")

        # Check final state
        final_balance = BillingManager.get_balance(org_id)
        final_remaining, final_total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Final - Balance: {final_balance} RUB, Limits: {final_remaining}/{final_total}")

if __name__ == "__main__":
    test_billing_api_direct()









