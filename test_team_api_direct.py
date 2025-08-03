



















#!/usr/bin/env python3

"""
Test Team Management API directly
"""

import uuid
import json
from web_server.app import app, db, Organization
from web_server.billing_models import OrganizationBalance, TariffPlan
from web_server.team_billing_manager import TeamBillingManager

def test_team_api():
    """Test team management API."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Team API",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Create a tariff plan with unique name
        tariff_name = f"Test Team Tariff {uuid.uuid4()}"
        tariff = TariffPlan(
            name=tariff_name,
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
            tariff_plan_id=tariff.id,
            team_members=1  # Initial team member
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Test team management API directly
        print("\nTesting Team API directly:")

        # Get initial team info
        try:
            team_info = TeamBillingManager.get_team_info(org_id)
            print(f"Initial team info: {team_info}")
        except Exception as e:
            print(f"Get initial team info: Failed - {str(e)}")

        # Add team member
        try:
            TeamBillingManager.add_team_member(org_id)
            print("Add team member: Success")
        except Exception as e:
            print(f"Add team member: Failed - {str(e)}")

        # Get team info after adding one member
        try:
            team_info = TeamBillingManager.get_team_info(org_id)
            print(f"Team info after adding one member: {team_info}")
        except Exception as e:
            print(f"Get team info: Failed - {str(e)}")

        # Add another team member
        try:
            TeamBillingManager.add_team_member(org_id)
            print("Add second team member: Success")
        except Exception as e:
            print(f"Add second team member: Failed - {str(e)}")

        # Get team info after adding two members
        try:
            team_info = TeamBillingManager.get_team_info(org_id)
            print(f"Team info after adding two members: {team_info}")
        except Exception as e:
            print(f"Get team info: Failed - {str(e)}")

        # Try to add too many team members (should fail)
        try:
            TeamBillingManager.add_team_member(org_id)
            print("Add third team member: Success")
        except Exception as e:
            print(f"Add third team member: Failed - {str(e)}")

        # Get team info after trying to add third member
        try:
            team_info = TeamBillingManager.get_team_info(org_id)
            print(f"Team info after trying to add third member: {team_info}")
        except Exception as e:
            print(f"Get team info: Failed - {str(e)}")

        # Remove team member
        try:
            TeamBillingManager.remove_team_member(org_id)
            print("Remove team member: Success")
        except Exception as e:
            print(f"Remove team member: Failed - {str(e)}")

        # Get team info after removing one member
        try:
            team_info = TeamBillingManager.get_team_info(org_id)
            print(f"Team info after removing one member: {team_info}")
        except Exception as e:
            print(f"Get team info: Failed - {str(e)}")

if __name__ == "__main__":
    test_team_api()





















