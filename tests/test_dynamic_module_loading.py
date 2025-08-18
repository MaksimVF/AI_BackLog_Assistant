



















import pytest
from pipelines.second_level_pipeline import SecondLevelPipeline
from pipelines.first_level_pipeline import FirstLevelPipeline
from level2.prioritization.prioritization_aggregator import PrioritizationAggregator
from level2.strategy.strategy_aggregator import StrategyAggregator

@pytest.mark.asyncio
async def test_second_level_dynamic_loading():
    # Создаем конвейер с динамической загрузкой модулей
    modules = {
        "prioritization": PrioritizationAggregator,
        "strategy": StrategyAggregator
    }
    pipeline = SecondLevelPipeline(modules=modules)
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    results = await pipeline.run(tasks)
    assert "prioritization" in results
    assert "strategy" in results
    assert "teamwork" not in results
    assert "analytics" not in results
    assert "visualization" not in results

@pytest.mark.asyncio
async def test_first_level_dynamic_loading():
    # Создаем конвейер с динамической загрузкой модулей
    modules = {
        "modality_processing": ModalityProcessingPipeline,
        "data_manipulation": DataManipulationPipeline,
        "data_output": DataOutputPipeline,
        "second_level": SecondLevelPipeline
    }
    pipeline = FirstLevelPipeline(modules=modules)
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10}
    ]
    results = await pipeline.run(tasks)
    assert "modality_processing" in results
    assert "data_manipulation" in results
    assert "data_output" in results
    assert "second_level" in results






















