






















import pytest
from fastapi.testclient import TestClient
from api.api import app
from pipelines.first_level_pipeline import FirstLevelPipeline
from pipelines.second_level_pipeline import SecondLevelPipeline

client = TestClient(app)

@pytest.mark.asyncio
async def test_pipeline_error_handling():
    pipeline = FirstLevelPipeline()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    # Временно ломаем один из модулей
    pipeline.modules["modality_processing"].run = lambda x: 1/0
    results = await pipeline.run(tasks)
    assert "error" in results["modality_processing"]

@pytest.mark.asyncio
async def test_second_level_error_handling():
    pipeline = SecondLevelPipeline()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    # Временно ломаем один из модулей
    pipeline.modules["prioritization"].run = lambda x: 1/0
    results = await pipeline.run(tasks)
    assert "error" in results["prioritization"]

def test_api_error_handling():
    response = client.post("/run_pipeline", json=[
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ])
    assert response.status_code == 500
    assert "error" in response.json()

























