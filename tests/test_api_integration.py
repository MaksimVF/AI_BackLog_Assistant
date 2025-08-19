

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from level2.api.router import router
from level2.dto import AnalysisConfig
from level2.repository.mock_repo import MockRepository
from level2.pipeline.orchestrator import Level2Orchestrator
from datetime import datetime

# Create a test version of the router that doesn't depend on SQLAlchemy
def create_test_app():
    app = FastAPI()

    # Create a simplified version of the analyze endpoint for testing
    @app.post("/level2/analyze")
    def analyze_test(req: dict):
        project_id = req.get("project_id")
        cfg_dict = req.get("config", {})
        cfg = AnalysisConfig(**cfg_dict)

        # Use mock repository
        repo = MockRepository()

        # Create test tasks
        tasks = [
            {
                "id": "task1",
                "project_id": project_id,
                "title": "High value, low effort task",
                "metadata": {
                    "value": "9",
                    "effort": "2",
                    "importance": "8",
                    "satisfaction": "3",
                    "priority": "85",
                    "moscow": "must"
                },
                "created_at": datetime.now()
            },
            {
                "id": "task2",
                "project_id": project_id,
                "title": "Medium priority task",
                "metadata": {
                    "value": "5",
                    "effort": "5",
                    "importance": "6",
                    "satisfaction": "4",
                    "priority": "50",
                    "moscow": "should"
                },
                "created_at": datetime.now()
            }
        ]

        repo.tasks = tasks

        # Create orchestrator and run analysis
        orch = Level2Orchestrator(repo)
        res = orch.analyze_project(project_id, cfg)
        return res.model_dump()

    return app

@pytest.fixture
def client():
    app = create_test_app()
    return TestClient(app)

def test_api_integration_all_agents(client):
    """Test that the API can handle all scoring agents"""
    response = client.post("/level2/analyze", json={
        "project_id": "test_project",
        "config": {
            "methods": ["RICE", "MOSCOW", "WSJF", "KANO", "VALUE_EFFORT", "OPPORTUNITY", "STACK_RANKING"],
            "weights": {
                "RICE": 1.0,
                "MOSCOW": 0.8,
                "WSJF": 1.0,
                "KANO": 1.0,
                "VALUE_EFFORT": 1.0,
                "OPPORTUNITY": 1.0,
                "STACK_RANKING": 0.9
            }
        },
        "async_mode": False
    })

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "project_id" in data
    assert "tasks" in data
    assert len(data["tasks"]) == 2

    # Verify that all requested methods are present
    for task in data["tasks"]:
        method_scores = task["method_scores"]
        method_names = [ms["method"] for ms in method_scores]

        expected_methods = ["RICE", "MOSCOW", "WSJF", "KANO", "VALUE_EFFORT", "OPPORTUNITY", "STACK_RANKING"]

        for method in expected_methods:
            assert method in method_names, f"Method {method} not found in task scores"

        # Verify that combined score is calculated
        assert "combined_score" in task
        assert task["combined_score"] is not None

        # Verify that labels are present
        assert "labels" in task
        assert len(task["labels"]) > 0

def test_api_integration_subset_agents(client):
    """Test that the API can handle a subset of scoring agents"""
    response = client.post("/level2/analyze", json={
        "project_id": "test_project",
        "config": {
            "methods": ["RICE", "WSJF", "VALUE_EFFORT"],
            "weights": {
                "RICE": 1.0,
                "WSJF": 1.0,
                "VALUE_EFFORT": 1.0
            }
        },
        "async_mode": False
    })

    assert response.status_code == 200
    data = response.json()

    # Verify that only requested methods are present
    for task in data["tasks"]:
        method_scores = task["method_scores"]
        method_names = [ms["method"] for ms in method_scores]

        expected_methods = ["RICE", "WSJF", "VALUE_EFFORT"]

        # Check that all requested methods are present
        for method in expected_methods:
            assert method in method_names

        # Check that no unexpected methods are present
        for method in method_names:
            assert method in expected_methods

