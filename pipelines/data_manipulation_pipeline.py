


















from typing import List, Dict, Any
from level2.prioritization.prioritization_aggregator import PrioritizationAggregator
from level2.strategy.strategy_aggregator import StrategyAggregator

class DataManipulationPipeline:
    """
    Конвейер манипуляции данными: приоритизация и категоризация задач.
    """

    def __init__(self):
        self.prioritization = PrioritizationAggregator()
        self.strategy = StrategyAggregator()

    async def run(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Запуск конвейера манипуляции данными.
        :param tasks: список задач в формате словарей
        :return: приоритизированные и категоризированные задачи
        """
        # Пример приоритизации и категоризации задач
        prioritization_results = await self.prioritization.run(tasks)
        strategy_results = await self.strategy.run(tasks)

        # Объединение результатов
        manipulated_tasks = []
        for task in tasks:
            manipulated_task = {
                **task,
                "prioritization": prioritization_results.get(task["id"], {}),
                "strategy": strategy_results.get(task["id"], {})
            }
            manipulated_tasks.append(manipulated_task)
        return manipulated_tasks




















