
















from typing import List, Dict, Any
from level2.prioritization.prioritization_aggregator import PrioritizationAggregator
from level2.strategy.strategy_aggregator import StrategyAggregator
from level2.teamwork.teamwork_aggregator import TeamworkAggregator
from level2.analytics.analytics_aggregator import AnalyticsAggregator
from level2.visualization.visualization_aggregator import VisualizationAggregator
from pipelines.second_level_pipeline import SecondLevelPipeline

class FirstLevelPipeline:
    """
    Первый уровень анализа: базовая обработка задач.
    """

    def __init__(self):
        self.prioritization = PrioritizationAggregator()
        self.strategy = StrategyAggregator()
        self.teamwork = TeamworkAggregator()
        self.analytics = AnalyticsAggregator()
        self.visualization = VisualizationAggregator()
        self.second_level = SecondLevelPipeline()

    async def run(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Запуск пайплайна первого уровня.
        :param tasks: список задач в формате словарей
        :return: словарь с результатами анализа
        """
        results = {}

        # Пример базовой обработки задач
        results["prioritization"] = await self.prioritization.run(tasks)
        results["strategy"] = await self.strategy.run(tasks)
        results["teamwork"] = await self.teamwork.run(tasks)
        results["analytics"] = await self.analytics.run(tasks)
        results["visualization"] = await self.visualization.run(tasks)

        # Запуск второго уровня анализа
        results["second_level"] = await self.second_level.run(tasks)

        return results


















