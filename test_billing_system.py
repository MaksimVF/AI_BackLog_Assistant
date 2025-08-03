



"""
Test Script for Billing System

This script demonstrates the billing system functionality.
"""

import uuid
import os
from web_server.app import app, db
from web_server.billing_manager import BillingManager
from web_server.billing_models import Organization, OrganizationBalance, TariffPlan, FeatureConfig
from agents.categorization.billed_categorization_agent import BilledCategorizationAgent

def setup_test_environment():
    """Set up test environment with sample data."""
    with app.app_context():
        # Create a test organization
        org_id = str(uuid.uuid4())
        org = Organization(
            id=org_id,
            name="Test Organization",
            created_by="test-user-id"
        )
        db.session.add(org)

        # Get the Free tariff plan
        tariff_plan = TariffPlan.query.filter_by(name="Free").first()

        # Create organization balance
        org_balance = OrganizationBalance(
            organization_id=org_id,
            balance_rub=100.0,  # Add some balance
            tariff_plan_id=tariff_plan.id if tariff_plan else None
        )
        db.session.add(org_balance)

        db.session.commit()

        print(f"Created test organization: {org_id}")
        return org_id

def test_billing_system():
    """Test the billing system functionality."""
    with app.app_context():
        # Setup test environment
        org_id = setup_test_environment()

        # Test 1: Check initial balance
        balance = BillingManager.get_balance(org_id)
        print(f"Initial balance: {balance} RUB")

        # Test 2: Check limits
        remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
        print(f"CategorizationAgent limits: {remaining}/{total} calls")

        # Test 3: Use the billed agent
        agent = BilledCategorizationAgent()
        test_document = "This is a test document for categorization."

        try:
            # This should work within the free limits
            result = agent.categorize_document(test_document)
            print("Categorization successful!")
            print(f"Result: {result}")

            # Check balance after usage
            new_balance = BillingManager.get_balance(org_id)
            print(f"Balance after categorization: {new_balance} RUB")

            # Check remaining limits
            remaining, total = BillingManager.check_limit(org_id, "CategorizationAgent")
            print(f"Remaining limits: {remaining}/{total} calls")

        except Exception as e:
            print(f"Error during categorization: {e}")

        # Test 4: Try to exceed limits
        print("\nTesting limit exhaustion...")
        try:
            # Use up the remaining limits
            for i in range(remaining + 10):  # Try to exceed limits
                try:
                    result = agent.categorize_document(f"Test document {i}")
                    print(f"Categorization {i+1} successful")
                except Exception as e:
                    print(f"Failed at categorization {i+1}: {e}")
                    break

        except Exception as e:
            print(f"Error during limit testing: {e}")

if __name__ == "__main__":
    # Set up the Flask app context
    os.environ['FLASK_APP'] = 'web_server.app'
    os.environ['FLASK_ENV'] = 'development'

    # Initialize the billing system
    from web_server.init_billing import init_billing_system
    init_billing_system()

    # Run the test
    test_billing_system()


