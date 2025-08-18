


















import pytest
from pipelines.modality_processing_pipeline import ModalityProcessingPipeline

@pytest.mark.asyncio
async def test_modality_processing_pipeline():
    pipeline = ModalityProcessingPipeline()
    tasks = [
        {"id": "T1", "title": "  Task 1  ", "status": "open", "value": "10", "effort": "5"},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": "20", "effort": "10"}
    ]
    cleaned_tasks = await pipeline.run(tasks)
    assert cleaned_tasks[0]["title"] == "Task 1"
    assert cleaned_tasks[0]["value"] == 10.0
    assert cleaned_tasks[0]["effort"] == 5.0
    assert cleaned_tasks[1]["title"] == "Task 2"
    assert cleaned_tasks[1]["value"] == 20.0
    assert cleaned_tasks[1]["effort"] == 10.0





















