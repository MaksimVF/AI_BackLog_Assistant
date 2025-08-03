



#!/usr/bin/env python3

"""
Test Billing System with Limit Exceed
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan

def test_limit_exceed():
    """Test billing when limits are exceeded."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Organization - Limit Exceed",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Get the Free tariff plan
        tariff_plan = TariffPlan.query.filter_by(name="Free").first()

        # Create organization balance with limited balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=5.0,  # Small balance to test PAYG
            tariff_plan_id=tariff_plan.id if tariff_plan else None
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Use up all the free limits for CategorizationAgent
        print("Using up free limits...")
        for i in range(100):  # Free plan has 100 calls
            try:
                amount_charged = BillingManager.charge(
                    organization_id=org_id,
                    feature_name="CategorizationAgent",
                    units=1,
                    user_id="test-user-id"
                )
                if i < 99:
                    print(f"Call {i+1}: Charged {amount_charged} RUB (from limits)")
                else:
                    print(f"Call {i+1}: Charged {amount_charged} RUB (PAYG)")
            except Exception as e:
                print(f"Error on call {i+1}: {e}")
                break

        # Check final balance
        final_balance = BillingManager.get_balance(org_id)
        print(f"Final balance: {final_balance} RUB")

        # Try to use more when balance is insufficient
        print("\nTesting insufficient balance...")
        try:
            amount_charged = BillingManager.charge(
                organization_id=org_id,
                feature_name="CategorizationAgent",
                units=10,  # Try to charge for 10 more calls
                user_id="test-user-id"
            )
            print(f"Charged {amount_charged} RUB for additional usage")
        except Exception as e:
            print(f"Error as expected: {e}")

if __name__ == "__main__":
    test_limit_exceed()



