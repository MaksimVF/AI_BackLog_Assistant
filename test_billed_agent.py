







#!/usr/bin/env python3

"""
Test Billed Agent Wrapper
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan
from agents.categorization.billed_categorization_agent import BilledCategorizationAgent

def test_billed_agent():
    """Test the billed agent wrapper."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Billed Agent",
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

        # Create billed agent
        billed_agent = BilledCategorizationAgent(organization_id=org_id, user_id="test-user-id")

        # Check initial state
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Initial state - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Test using the agent within limits
        print("\nTesting within limits...")
        for i in range(5):
            try:
                result = billed_agent.categorize_text(f"Test text {i+1}")
                print(f"Call {i+1}: Success - {result}")
            except Exception as e:
                print(f"Call {i+1}: Error - {e}")
                break

        # Check state after using within limits
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"After 5 calls - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Use up all limits
        print("\nUsing up all limits...")
        for i in range(95):  # Use up the remaining 95 calls
            try:
                result = billed_agent.categorize_text(f"Test text {i+6}")
                if i % 10 == 0:
                    print(f"Call {i+6}: Success")
            except Exception as e:
                print(f"Call {i+6}: Error - {e}")
                break

        # Check state after using all limits
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"After using all limits - Balance: {balance} RUB, Limits: {remaining}/{total}")

        # Test beyond limits (should charge from balance)
        print("\nTesting beyond limits...")
        for i in range(3):
            try:
                result = billed_agent.categorize_text(f"Test text beyond limits {i+1}")
                print(f"Beyond limits call {i+1}: Success - {result}")
            except Exception as e:
                print(f"Beyond limits call {i+1}: Error - {e}")
                break

        # Check final state
        balance = BillingManager.get_balance(org_id)
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"Final state - Balance: {balance} RUB, Limits: {remaining}/{total}")

if __name__ == "__main__":
    test_billed_agent()







