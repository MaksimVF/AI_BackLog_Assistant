





#!/usr/bin/env python3

"""
Debug Check Limit Method
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan, UsageLog

def debug_check_limit():
    """Debug check_limit method."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Debug Check Limit",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Get the Free tariff plan
        tariff_plan = TariffPlan.query.filter_by(name="Free").first()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=10.0,
            tariff_plan_id=tariff_plan.id if tariff_plan else None
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Check initial limits
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Initial limits: {remaining}/{total}")

        # Use up all but 1 of the free limits
        for i in range(99):
            # Check limits before charge
            remaining_before, total_before = BillingManager.check_limit(org_id, "CategorizationAgent")

            # Charge
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=1,
                user_id="test-user-id"
            )

            # Check limits after charge
            remaining_after, total_after = BillingManager.check_limit(org_id, "CategorizationAgent")

            if i >= 95:  # Show detailed info for last few calls
                print(f"Call {i+1}:")
                print(f"  Before: {remaining_before}/{total_before}")
                print(f"  Charged: {amount_charged} RUB")
                print(f"  After: {remaining_after}/{total_after}")

        # Now we should be at 1 remaining
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"\nBefore 100th call: {remaining}/{total}")

        # Make the 100th call
        remaining_before, total_before = BillingManager.check_limit(org_id, "CategorizationAgent")
        amount_charged = BillingManager.charge(
            organization_id=org_id,
            feature_name="CategorizationAgent",
            units=1,
            user_id="test-user-id"
        )
        remaining_after, total_after = BillingManager.check_limit(org_id, "CategorizationAgent")

        print(f"Call 100:")
        print(f"  Before: {remaining_before}/{total_before}")
        print(f"  Charged: {amount_charged} RUB")
        print(f"  After: {remaining_after}/{total_after}")

        # Check balance
        balance = BillingManager.get_balance(org_id)
        print(f"Balance: {balance} RUB")

if __name__ == "__main__":
    debug_check_limit()





