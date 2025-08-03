













#!/usr/bin/env python3

"""
Test Token-Based Billing System
"""

import uuid
from web_server.app import app, db, Organization
from web_server.billing_models import OrganizationBalance, TariffPlan
from web_server.token_billing_manager import TokenBasedBillingManager
from web_server.token_monitors import CombinedTokenMonitor
from web_server.team_billing_manager import TeamBillingManager
from web_server.billed_pipeline_example import BilledInformationPipeline

def test_token_billing():
    """Test token-based billing system."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Token Billing",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Create a tariff plan
        tariff = TariffPlan(
            name="Test Token Tariff",
            price_per_month=0.0,
            included_limits={"token_usage": 1000},
            discounts={},
            access_features=[],
            max_team_members=5,
            member_price=10.0
        )
        db.session.add(tariff)
        db.session.commit()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=100.0,
            tariff_plan_id=tariff.id
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Test token-based billing
        print("\nTesting Token-Based Billing:")

        # Test direct token charging
        cost = TokenBasedBillingManager.charge_tokens(
            org_id,
            input_tokens=100,
            llm_tokens=50,
            output_tokens=20,
            user_id="test-user-id"
        )
        print(f"Charged {cost} RUB for token usage")

        # Check new balance
        new_balance = OrganizationBalance.query.get(org_id).balance_rub
        print(f"New balance: {new_balance} RUB")

        # Test token monitors
        print("\nTesting Token Monitors:")
        monitor = CombinedTokenMonitor(org_id, "test-user-id")
        monitor.monitor(input_tokens=50, llm_tokens=20, output_tokens=10)
        print("Token monitor test completed")

        # Check balance after monitor
        monitor_balance = OrganizationBalance.query.get(org_id).balance_rub
        print(f"Balance after monitor: {monitor_balance} RUB")

        # Test team billing
        print("\nTesting Team Billing:")

        # Add team members
        try:
            TeamBillingManager.add_team_member(org_id)
            print("Added team member 1")
            TeamBillingManager.add_team_member(org_id)
            print("Added team member 2")
        except Exception as e:
            print(f"Error adding team member: {e}")

        # Check team info
        team_info = TeamBillingManager.get_team_info(org_id)
        print(f"Team info: {team_info}")

        # Test billed pipeline
        print("\nTesting Billed Pipeline:")
        pipeline = BilledInformationPipeline(org_id, "test-user-id")
        result = pipeline.process("This is a test input with several tokens to process")
        print(f"Pipeline result: {result}")

        # Check final balance
        final_balance = OrganizationBalance.query.get(org_id).balance_rub
        print(f"Final balance: {final_balance} RUB")

if __name__ == "__main__":
    test_token_billing()













