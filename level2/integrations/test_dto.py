




"""
Test script for integration DTO models.
"""

import os
import sys
from datetime import datetime

# Add the level2 directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.integration_dto import IntegrationConfig, IntegrationStatus, SyncRequest, JiraConfig, TrelloConfig

def test_integration_dto():
    """Test the integration DTO models."""
    print("Testing integration DTO models...")

    # Test Jira config
    jira_config = JiraConfig(
        base_url="https://test.atlassian.net",
        username="test_user",
        api_token="test_token",
        project_key="TEST"
    )
    assert jira_config.service == "jira"
    assert jira_config.base_url == "https://test.atlassian.net"
    print("✓ Jira config DTO test passed")

    # Test Trello config
    trello_config = TrelloConfig(
        api_key="test_key",
        api_token="test_token",
        board_id="test_board"
    )
    assert trello_config.service == "trello"
    assert trello_config.api_key == "test_key"
    print("✓ Trello config DTO test passed")

    # Test sync request
    sync_request = SyncRequest(
        service="jira",
        task_ids=["test_task_123"]
    )
    assert sync_request.service == "jira"
    assert sync_request.task_ids == ["test_task_123"]
    print("✓ Sync request DTO test passed")

    # Test status response
    status = IntegrationStatus(
        service="jira",
        connected=True,
        last_sync=datetime.now(),
        tasks_synced=5
    )
    assert status.service == "jira"
    assert status.connected == True
    assert status.tasks_synced == 5
    print("✓ Status response DTO test passed")

def main():
    """Run all DTO tests."""
    print("Running integration DTO tests...")
    print("=" * 50)

    test_integration_dto()

    print("=" * 50)
    print("✓ All integration DTO tests completed!")

if __name__ == "__main__":
    main()




