















from level2.prioritization.prioritization_aggregator import PrioritizationAggregator
from level2.strategy.strategy_aggregator import StrategyAggregator
from level2.teamwork.teamwork_aggregator import TeamworkAggregator
from level2.analytics.analytics_aggregator import AnalyticsAggregator
from level2.visualization.visualization_aggregator import VisualizationAggregator

class SecondLevelPipeline:
    """
    Второй уровень анализа: углублённая аналитика и прогнозирование.
    Управляет всеми агрегаторами (модулями).
    """

    def __init__(self):
        self.prioritization = PrioritizationAggregator()
        self.strategy = StrategyAggregator()
        self.teamwork = TeamworkAggregator()
        self.analytics = AnalyticsAggregator()
        self.visualization = VisualizationAggregator()

    async def run(self, tasks: list, modules: list = None) -> dict:
        """
        Запуск пайплайна второго уровня.
        :param tasks: список задач в формате словарей
        :param modules: список модулей, которые нужно запустить
                        ("prioritization", "strategy", "teamwork", "analytics", "visualization")
                        Если None — запускаются все.
        :return: словарь с результатами анализа
        """
        results = {}

        if modules is None or "prioritization" in modules:
            results["prioritization"] = await self.prioritization.run(tasks)

        if modules is None or "strategy" in modules:
            results["strategy"] = await self.strategy.run(tasks)

        if modules is None or "teamwork" in modules:
            results["teamwork"] = await self.teamwork.run(tasks)

        if modules is None or "analytics" in modules:
            results["analytics"] = await self.analytics.run(tasks)

        if modules is None or "visualization" in modules:
            results["visualization"] = await self.visualization.run(tasks)

        return results

















