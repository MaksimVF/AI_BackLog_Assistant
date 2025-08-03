






#!/usr/bin/env python3

"""
Debug Beyond Limit
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan, UsageLog

def debug_beyond_limit():
    """Debug what happens when we go beyond the limit."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Debug Beyond Limit",
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

        # Use up all the free limits
        for i in range(100):
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=1,
                user_id="test-user-id"
            )

        print("Used up all 100 free limits")

        # Check balance and limits
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Balance: {balance} RUB")
        print(f"Limits: {remaining}/{total}")

        # Now try to use more (should charge from balance)
        print("\nTrying to use beyond limits...")
        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=1,
                user_id="test-user-id"
            )
            print(f"Charged {amount_charged} RUB for additional usage")

            # Check new balance
            new_balance = BillingManager.get_balance(org_id)
            print(f"New balance: {new_balance} RUB")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_beyond_limit()






