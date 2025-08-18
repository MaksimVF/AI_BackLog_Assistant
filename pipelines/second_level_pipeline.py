



















from typing import Dict, Type
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

    def __init__(self, modules: Dict[str, Type] = None):
        """
        Инициализация конвейера с динамической загрузкой модулей.
        :param modules: словарь модулей, где ключ — имя модуля, значение — класс модуля
        """
        if modules is None:
            modules = {
                "prioritization": PrioritizationAggregator,
                "strategy": StrategyAggregator,
                "teamwork": TeamworkAggregator,
                "analytics": AnalyticsAggregator,
                "visualization": VisualizationAggregator
            }
        self.modules = {name: cls() for name, cls in modules.items()}

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

        if modules is None:
            modules = list(self.modules.keys())

        for module in modules:
            if module in self.modules:
                results[module] = await self.modules[module].run(tasks)

        return results





















