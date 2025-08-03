









#!/usr/bin/env python3

"""
Test Billing API
"""

import uuid
import requests
from web_server.app import app, db, Organization
from web_server.billing_manager import BillingManager
from web_server.billing_models import OrganizationBalance, TariffPlan

def test_billing_api():
    """Test billing API endpoints."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test API Organization",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Get the Free tariff plan
        tariff_plan = TariffPlan.query.filter_by(name="Free").first()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=5.0,
            tariff_plan_id=tariff_plan.id if tariff_plan else None
        )
        db.session.add(org_balance)
        db.session.commit()

        print(f"Created test organization: {org_id}")

        # Start Flask app in a separate thread
        import threading
        import time

        def run_flask():
            app.run(port=5002, debug=False)

        thread = threading.Thread(target=run_flask)
        thread.daemon = True
        thread.start()

        # Wait for server to start
        time.sleep(3)

        # Test API endpoints
        base_url = "http://localhost:5002/api/v1/billing"

        # Test status endpoint
        try:
            response = requests.get(f"{base_url}/status")
            print(f"Status endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Status endpoint error: {e}")

        # Test balance endpoint
        try:
            response = requests.get(f"{base_url}/balance/{org_id}")
            print(f"Balance endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Balance endpoint error: {e}")

        # Test limits endpoint
        try:
            response = requests.get(f"{base_url}/limits/{org_id}")
            print(f"Limits endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Limits endpoint error: {e}")

        # Test usage endpoint
        try:
            response = requests.get(f"{base_url}/usage/{org_id}")
            print(f"Usage endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Usage endpoint error: {e}")

        # Test charge endpoint
        try:
            response = requests.post(f"{base_url}/charge/{org_id}/CategorizationAgent", json={"units": 1, "user_id": "test-user-id"})
            print(f"Charge endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Charge endpoint error: {e}")

if __name__ == "__main__":
    test_billing_api()









