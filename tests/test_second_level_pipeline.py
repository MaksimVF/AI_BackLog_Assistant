
















import pytest
from pipelines.second_level_pipeline import SecondLevelPipeline

@pytest.mark.asyncio
async def test_second_level_pipeline_all_modules():
    pipeline = SecondLevelPipeline()
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

@pytest.mark.asyncio
async def test_second_level_pipeline_selected_modules():
    pipeline = SecondLevelPipeline()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5, "dependencies": ["T2"],
         "start_date": "2023-01-01", "end_date": "2023-01-10"},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10, "dependencies": [],
         "start_date": "2023-01-05", "end_date": "2023-01-15"}
    ]
    results = await pipeline.run(tasks, modules=["prioritization", "visualization"])
    assert "prioritization" in results
    assert "strategy" not in results
    assert "teamwork" not in results
    assert "analytics" not in results
    assert "visualization" in results

@pytest.mark.asyncio
async def test_second_level_pipeline_empty_modules():
    pipeline = SecondLevelPipeline()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5, "dependencies": ["T2"],
         "start_date": "2023-01-01", "end_date": "2023-01-10"},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10, "dependencies": [],
         "start_date": "2023-01-05", "end_date": "2023-01-15"}
    ]
    results = await pipeline.run(tasks, modules=[])
    assert results == {}
















