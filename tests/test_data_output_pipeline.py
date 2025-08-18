




















import pytest
from pipelines.data_output_pipeline import DataOutputPipeline

@pytest.mark.asyncio
async def test_data_output_pipeline():
    pipeline = DataOutputPipeline()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    prepared_tasks = await pipeline.run(tasks)
    assert prepared_tasks[0]["prepared"] == True
    assert prepared_tasks[1]["prepared"] == True






















