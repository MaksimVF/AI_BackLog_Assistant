





















from typing import Dict, Type
from config.config import PipelineConfig, AgentConfig
from level2.prioritization.prioritization_aggregator import PrioritizationAggregator
from level2.strategy.strategy_aggregator import StrategyAggregator
from level2.teamwork.teamwork_aggregator import TeamworkAggregator
from level2.analytics.analytics_aggregator import AnalyticsAggregator
from level2.visualization.visualization_aggregator import VisualizationAggregator
import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SecondLevelPipeline:
    """
    Второй уровень анализа: углублённая аналитика и прогнозирование.
    Управляет всеми агрегаторами (модулями).
    """

    def __init__(self, config: PipelineConfig = None):
        """
        Инициализация конвейера с конфигурацией.
        :param config: конфигурация конвейера
        """
        if config is None:
            config = PipelineConfig(
                name="second_level",
                agents=[
                    AgentConfig(name="prioritization", enabled=True),
                    AgentConfig(name="strategy", enabled=True),
                    AgentConfig(name="teamwork", enabled=True),
                    AgentConfig(name="analytics", enabled=True),
                    AgentConfig(name="visualization", enabled=True)
                ]
            )
        self.config = config
        self.modules = {}
        for agent in self.config.agents:
            if agent.enabled:
                try:
                    module_class = globals()[agent.name.capitalize() + "Aggregator"]
                    self.modules[agent.name] = module_class()
                except KeyError:
                    logger.error(f"Module {agent.name} not found")
                except Exception as e:
                    logger.error(f"Error initializing module {agent.name}: {e}")

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
                try:
                    results[module] = await self.modules[module].run(tasks)
                except Exception as e:
                    logger.error(f"Error running module {module}: {e}")
                    results[module] = {"error": str(e)}

        return results























