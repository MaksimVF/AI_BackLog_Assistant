
















#!/usr/bin/env python3

"""
Test Team Management API
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

        # Create a tariff plan
        tariff = TariffPlan(
            name="Test Team Tariff",
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

        # Test team management API
        with app.test_client() as client:
            # Test adding team members
            print("\nTesting Team API:")

            # Add team member
            response = client.post(f'/api/v1/team/members?org_id={org_id}')
            print(f"Add team member response: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            # Add another team member
            response = client.post(f'/api/v1/team/members?org_id={org_id}')
            print(f"Add second team member response: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            # Get team info
            response = client.get(f'/api/v1/team/info?org_id={org_id}')
            print(f"Team info response: {response.status_code}")
            print(f"Team info data: {response.get_data(as_text=True)}")

            # Try to add too many team members (should fail)
            response = client.post(f'/api/v1/team/members?org_id={org_id}')
            print(f"Add third team member response: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

            # Remove team member
            response = client.delete(f'/api/v1/team/members?org_id={org_id}')
            print(f"Remove team member response: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_team_api()
















