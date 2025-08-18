













from typing import List, Dict, Any, Optional
from .trend_analysis import TrendAnalysisAgent
from .risk_analysis import RiskAnalysisAgent
from .dependency_mapping import DependencyMappingAgent
from .effort_forecasting import EffortForecastingAgent
from .forensic_analysis import ForensicAnalysisAgent

class AnalyticsAggregator:
    """
    Агрегатор для модулей аналитики и прогнозирования (второй уровень).
    """

    def __init__(self):
        self.trend_agent = TrendAnalysisAgent()
        self.risk_agent = RiskAnalysisAgent()
        self.dependency_agent = DependencyMappingAgent()
        self.effort_agent = EffortForecastingAgent()
        self.forensic_agent = ForensicAnalysisAgent()

    async def run(self, tasks: List[Dict], history: List[Dict] = None) -> Dict[str, Any]:
        """
        Запуск всех аналитических агентов.
        :param tasks: список задач
        :param history: история задач для ретроспективного анализа
        :return: агрегированные результаты
        """
        results = {}

        results["trends"] = await self.trend_agent.run(tasks)
        results["risks"] = await self.risk_agent.run(tasks)
        results["dependencies"] = await self.dependency_agent.run(tasks)
        results["effort_forecast"] = await self.effort_agent.run(tasks)

        if history:
            results["forensic"] = await self.forensic_agent.run(history)

        return results













