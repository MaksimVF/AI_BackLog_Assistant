



















import pytest
from pipelines.data_manipulation_pipeline import DataManipulationPipeline

@pytest.mark.asyncio
async def test_data_manipulation_pipeline():
    pipeline = DataManipulationPipeline()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    manipulated_tasks = await pipeline.run(tasks)
    assert "prioritization" in manipulated_tasks[0]
    assert "strategy" in manipulated_tasks[0]
    assert "prioritization" in manipulated_tasks[1]
    assert "strategy" in manipulated_tasks[1]























