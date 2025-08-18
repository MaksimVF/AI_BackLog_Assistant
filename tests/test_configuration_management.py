




















import pytest
from pipelines.second_level_pipeline import SecondLevelPipeline
from pipelines.first_level_pipeline import FirstLevelPipeline
from config.config import PipelineConfig, AgentConfig

@pytest.mark.asyncio
async def test_second_level_configuration():
    # Создаем конфигурацию с отключенными модулями
    config = PipelineConfig(
        name="second_level",
        agents=[
            AgentConfig(name="prioritization", enabled=True),
            AgentConfig(name="strategy", enabled=False),
            AgentConfig(name="teamwork", enabled=True),
            AgentConfig(name="analytics", enabled=False),
            AgentConfig(name="visualization", enabled=True)
        ]
    )
    pipeline = SecondLevelPipeline(config=config)
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    results = await pipeline.run(tasks)
    assert "prioritization" in results
    assert "teamwork" in results
    assert "visualization" in results
    assert "strategy" not in results
    assert "analytics" not in results

@pytest.mark.asyncio
async def test_first_level_configuration():
    # Создаем конфигурацию с отключенными модулями
    config = PipelineConfig(
        name="first_level",
        agents=[
            AgentConfig(name="modality_processing", enabled=True),
            AgentConfig(name="data_manipulation", enabled=False),
            AgentConfig(name="data_output", enabled=True),
            AgentConfig(name="second_level", enabled=False)
        ]
    )
    pipeline = FirstLevelPipeline(config=config)
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    results = await pipeline.run(tasks)
    assert "modality_processing" in results
    assert "data_output" in results
    assert "data_manipulation" not in results
    assert "second_level" not in results























