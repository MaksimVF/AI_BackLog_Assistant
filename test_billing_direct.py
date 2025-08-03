









#!/usr/bin/env python3

"""
Test Billing Directly
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan

def test_billing_direct():
    """Test billing directly with BillingManager."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Billing Direct",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Get the Free tariff plan
        tariff_plan = TariffPlan.query.filter_by(name="Free").first()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=5.0,  # Small balance for testing
            tariff_plan_id=tariff_plan.id if tariff_plan else None
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Check initial state
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Initial state - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Test charging within limits
        print("\nTesting charging within limits...")
        for i in range(100):  # Use up all 100 free calls
            try:
                amount_charged = BillingManager.charge(
                    organization_id=org_id,
                    feature_name="CategorizationAgent",
                    units=1,
                    user_id="test-user-id"
                )
                if i % 10 == 0:
                    print(f"Call {i+1}: Charged {amount_charged} RUB")
            except Exception as e:
                print(f"Call {i+1}: Error - {e}")
                break

        # Check state after using all limits
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"After 100 calls - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Test beyond limits (should charge from balance)
        print("\nTesting beyond limits...")

        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=1,
                user_id="test-user-id"
            )
            print(f"Call 101: Charged {amount_charged} RUB")
        except Exception as e:
            print(f"Call 101: Error - {e}")

        # Check state after beyond limits call
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"After 101 calls - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Test with insufficient balance
        print("\nTesting with insufficient balance...")

        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=10,  # Try to use 10 units (would cost 10 RUB, but we have 4 RUB)
                user_id="test-user-id"
            )
            print(f"Large call: Charged {amount_charged} RUB")
        except Exception as e:
            print(f"Large call: Error (expected) - {e}")

        # Test premium feature access
        print("\nTesting premium feature access...")

        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="SmartSummaryAgent",  # Premium feature
                units=1,
                user_id="test-user-id"
            )
            print(f"Premium feature: Charged {amount_charged} RUB")
        except Exception as e:
            print(f"Premium feature: Error - {e}")

        # Test exclusive feature access (should fail on Free plan)
        print("\nTesting exclusive feature access...")

        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CodeRefactorAgent",  # Exclusive feature
                units=1,
                user_id="test-user-id"
            )
            print(f"Exclusive feature: Charged {amount_charged} RUB")
        except Exception as e:
            print(f"Exclusive feature: Error (expected) - {e}")

if __name__ == "__main__":
    test_billing_direct()









