




#!/usr/bin/env python3

"""
Debug Limit Calculation
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan, UsageLog

def debug_limit():
    """Debug limit calculation."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Debug Organization",
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
        print(f"Tariff plan: {tariff_plan.name}")
        print(f"CategorizationAgent limit: {tariff_plan.included_limits.get('CategorizationAgent', 'Not found')}")

        # Check initial limits
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Initial limits: {remaining}/{total}")

        # Use up all but 1 of the free limits
        for i in range(99):
            try:
                amount_charged = BillingManager.charge(
                    organization_id=org_id,
                    feature_name="CategorizationAgent",
                    units=1,
                    user_id="test-user-id"
                )
                if i < 98:
                    if i % 10 == 0:
                        print(f"Call {i+1}: Charged {amount_charged} RUB (from limits)")
                else:
                    print(f"Call {i+1}: Charged {amount_charged} RUB (should be from limits)")

                # Check limits after each charge
                remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
                if i % 10 == 0 or i >= 95:
                    print(f"After call {i+1}: {remaining}/{total}")

            except Exception as e:
                print(f"Error on call {i+1}: {e}")
                break

        # Check final state
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Final limits before 100th call: {remaining}/{total}")

        balance = BillingManager.get_balance(org_id)
        print(f"Balance before 100th call: {balance} RUB")

        # Now make the 100th call (should be the limit)
        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=1,
                user_id="test-user-id"
            )
            print(f"Call 100: Charged {amount_charged} RUB (should be from balance)")

            # Check state after 100th call
            remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
            print(f"Limits after 100th call: {remaining}/{total}")

            balance = BillingManager.get_balance(org_id)
            print(f"Balance after 100th call: {balance} RUB")

        except Exception as e:
            print(f"Error on 100th call: {e}")

if __name__ == "__main__":
    debug_limit()




