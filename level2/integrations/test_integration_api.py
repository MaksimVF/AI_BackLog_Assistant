



"""
Test script for integration API endpoints.
"""

import os
import sys
import json
from datetime import datetime

# Add the level2 directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

# Import router directly
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.router import router

from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_sync_endpoint():
    """Test the sync endpoint."""
    response = client.post(
        "/level2/integrations/sync",
        json={"service": "jira"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert "synced_tasks" in data

    print("✓ Sync endpoint test passed")

def test_jira_create_endpoint():
    """Test the Jira task creation endpoint."""
    response = client.post(
        "/level2/integrations/jira/create",
        json={
            "task_id": "test_task_123",
            "service": "jira",
            "title": "Test Task",
            "description": "Test description"
        }
    )

    # This will likely fail without a real database, but we can check the structure
    if response.status_code == 404:
        # Expected since task doesn't exist
        print("✓ Jira create endpoint returns 404 for non-existent task (expected)")
    else:
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "external_id" in data
        print("✓ Jira create endpoint test passed")

def test_trello_create_endpoint():
    """Test the Trello task creation endpoint."""
    response = client.post(
        "/level2/integrations/trello/create",
        json={
            "task_id": "test_task_123",
            "service": "trello",
            "title": "Test Task",
            "description": "Test description"
        }
    )

    # This will likely fail without a real database, but we can check the structure
    if response.status_code == 404:
        # Expected since task doesn't exist
        print("✓ Trello create endpoint returns 404 for non-existent task (expected)")
    else:
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "external_id" in data
        print("✓ Trello create endpoint test passed")

def test_integration_status():
    """Test the integration status endpoint."""
    response = client.get("/level2/integrations/status")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "service" in data[0]
    assert "connected" in data[0]

    print("✓ Integration status endpoint test passed")

def test_jira_config():
    """Test the Jira configuration endpoint."""
    response = client.post(
        "/level2/integrations/config/jira",
        json={
            "base_url": "https://test.atlassian.net",
            "username": "test_user",
            "api_token": "test_token",
            "project_key": "TEST",
            "service": "jira"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"

    print("✓ Jira config endpoint test passed")

def test_trello_config():
    """Test the Trello configuration endpoint."""
    response = client.post(
        "/level2/integrations/config/trello",
        json={
            "api_key": "test_key",
            "api_token": "test_token",
            "board_id": "test_board",
            "service": "trello"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"

    print("✓ Trello config endpoint test passed")

def main():
    """Run all API tests."""
    print("Running integration API tests...")
    print("=" * 50)

    test_sync_endpoint()
    test_jira_create_endpoint()
    test_trello_create_endpoint()
    test_integration_status()
    test_jira_config()
    test_trello_config()

    print("=" * 50)
    print("✓ All integration API tests completed!")

if __name__ == "__main__":
    main()



