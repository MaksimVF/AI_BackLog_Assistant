








#!/usr/bin/env python3

"""
Test Billing Middleware
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan
from web_server.billing_middleware import bill_feature_usage

def test_billing_middleware():
    """Test the billing middleware."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Billing Middleware",
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

        # Test billing middleware within limits
        print("\nTesting billing middleware within limits...")

        @bill_feature_usage(feature_name="CategorizationAgent", units=1)
        def test_function_within_limits():
            return "Function executed successfully"

        try:
            result = test_function_within_limits(org_id, "test-user-id")
            print(f"Function result: {result}")
        except Exception as e:
            print(f"Error: {e}")

        # Check state after first call
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"After 1 call - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Use up all but 1 of the limits
        print("\nUsing up most limits...")

        for i in range(98):  # Use up 98 more calls (99 total)
            try:
                result = test_function_within_limits(org_id, "test-user-id")
                if i % 20 == 0:
                    print(f"Call {i+2}: Success")
            except Exception as e:
                print(f"Call {i+2}: Error - {e}")
                break

        # Check state after using most limits
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"After 99 calls - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Test beyond limits (should charge from balance)
        print("\nTesting beyond limits...")

        @bill_feature_usage(feature_name="CategorizationAgent", units=1)
        def test_function_beyond_limits():
            return "Function executed beyond limits"

        try:
            result = test_function_beyond_limits(org_id, "test-user-id")
            print(f"Beyond limits result: {result}")
        except Exception as e:
            print(f"Beyond limits error: {e}")

        # Check final state
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Final state - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Test with insufficient balance
        print("\nTesting with insufficient balance...")

        @bill_feature_usage(feature_name="CategorizationAgent", units=10)  # Try to use 10 units
        def test_function_insufficient_balance():
            return "This should not execute"

        try:
            result = test_function_insufficient_balance(org_id, "test-user-id")
            print(f"Insufficient balance result: {result}")
        except Exception as e:
            print(f"Insufficient balance error (expected): {e}")

if __name__ == "__main__":
    test_billing_middleware()








