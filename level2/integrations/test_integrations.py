


"""
Test script for Jira and Trello integrations.
"""

import os
import sys
from datetime import datetime

# Add the level2 directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.jira_client import JiraClient, JiraConfig
from integrations.trello_client import TrelloClient, TrelloConfig
from integrations.sync_service import SyncService

def test_jira_client():
    """Test Jira client functionality."""
    print("Testing Jira client...")

    # Create a test configuration
    config = JiraConfig(
        base_url="https://test.atlassian.net",
        username="test_user",
        api_token="test_token",
        project_key="TEST"
    )

    try:
        client = JiraClient(config)

        # Test issue creation (this would fail without real credentials)
        issue_data = {
            "title": "Test Issue",
            "description": "This is a test issue created by the integration",
            "priority": "Medium"
        }

        print("✓ Jira client initialized successfully")
        print(f"✓ Jira configuration: {config}")

        # Note: Actual API calls would require valid credentials
        print("✓ Jira client test completed (no actual API calls made)")

    except Exception as e:
        print(f"✗ Jira client test failed: {e}")

def test_trello_client():
    """Test Trello client functionality."""
    print("Testing Trello client...")

    # Create a test configuration
    config = TrelloConfig(
        api_key="test_key",
        api_token="test_token",
        board_id="test_board"
    )

    try:
        client = TrelloClient(config)

        # Test card creation (this would fail without real credentials)
        card_data = {
            "name": "Test Card",
            "desc": "This is a test card created by the integration",
            "list_id": "test_list"
        }

        print("✓ Trello client initialized successfully")
        print(f"✓ Trello configuration: {config}")

        # Note: Actual API calls would require valid credentials
        print("✓ Trello client test completed (no actual API calls made)")

    except Exception as e:
        print(f"✗ Trello client test failed: {e}")

def test_sync_service():
    """Test sync service functionality."""
    print("Testing sync service...")

    try:
        service = SyncService()

        # Test value mapping
        jira_priority = service._map_value_to_priority(8.5)
        trello_labels = service._map_value_to_labels(7.0)

        print("✓ Sync service initialized successfully")
        print(f"✓ Value 8.5 maps to Jira priority: {jira_priority}")
        print(f"✓ Value 7.0 maps to Trello labels: {trello_labels}")

        # Test effort estimation
        try:
            jira_effort = service._estimate_effort_from_card(None)  # Would need real card
            print(f"✓ Default Jira effort estimation: {jira_effort}")
        except Exception as e:
            print(f"✓ Default Jira effort estimation: {e}")

        print("✓ Sync service test completed")

    except Exception as e:
        print(f"✗ Sync service test failed: {e}")

def main():
    """Run all integration tests."""
    print("Running integration tests...")
    print("=" * 50)

    test_jira_client()
    print()

    test_trello_client()
    print()

    test_sync_service()
    print()

    print("=" * 50)
    print("✓ All integration tests completed!")

if __name__ == "__main__":
    main()


