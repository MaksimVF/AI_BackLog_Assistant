

















import pytest
from pipelines.first_level_pipeline import FirstLevelPipeline

@pytest.mark.asyncio
async def test_first_level_pipeline():
    pipeline = FirstLevelPipeline()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5, "dependencies": ["T2"],
         "start_date": "2023-01-01", "end_date": "2023-01-10"},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10, "dependencies": [],
         "start_date": "2023-01-05", "end_date": "2023-01-15"}
    ]
    results = await pipeline.run(tasks)
    assert "prioritization" in results
    assert "strategy" in results
    assert "teamwork" in results
    assert "analytics" in results
    assert "visualization" in results
    assert "second_level" in results
    assert "prioritization" in results["second_level"]
    assert "strategy" in results["second_level"]
    assert "teamwork" in results["second_level"]
    assert "analytics" in results["second_level"]
    assert "visualization" in results["second_level"]


















