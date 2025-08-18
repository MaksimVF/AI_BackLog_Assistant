




















from typing import List, Dict, Any, Type
from level2.prioritization.prioritization_aggregator import PrioritizationAggregator
from level2.strategy.strategy_aggregator import StrategyAggregator
from level2.teamwork.teamwork_aggregator import TeamworkAggregator
from level2.analytics.analytics_aggregator import AnalyticsAggregator
from level2.visualization.visualization_aggregator import VisualizationAggregator
from pipelines.second_level_pipeline import SecondLevelPipeline
from pipelines.modality_processing_pipeline import ModalityProcessingPipeline
from pipelines.data_manipulation_pipeline import DataManipulationPipeline
from pipelines.data_output_pipeline import DataOutputPipeline

class FirstLevelPipeline:
    """
    Первый уровень анализа: базовая обработка задач.
    """

    def __init__(self, modules: Dict[str, Type] = None):
        """
        Инициализация конвейера с динамической загрузкой модулей.
        :param modules: словарь модулей, где ключ — имя модуля, значение — класс модуля
        """
        if modules is None:
            modules = {
                "modality_processing": ModalityProcessingPipeline,
                "data_manipulation": DataManipulationPipeline,
                "data_output": DataOutputPipeline,
                "second_level": SecondLevelPipeline
            }
        self.modules = {name: cls() for name, cls in modules.items()}

    async def run(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Запуск пайплайна первого уровня.
        :param tasks: список задач в формате словарей
        :return: словарь с результатами анализа
        """
        results = {}

        # Обработка модальностей
        cleaned_tasks = await self.modules["modality_processing"].run(tasks)
        results["modality_processing"] = cleaned_tasks

        # Манипуляция данными
        manipulated_tasks = await self.modules["data_manipulation"].run(cleaned_tasks)
        results["data_manipulation"] = manipulated_tasks

        # Вывод данных
        prepared_tasks = await self.modules["data_output"].run(manipulated_tasks)
        results["data_output"] = prepared_tasks

        # Запуск второго уровня анализа
        results["second_level"] = await self.modules["second_level"].run(prepared_tasks)

        return results






















