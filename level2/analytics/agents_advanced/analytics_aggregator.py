











from typing import Dict, Any, List, Tuple, Optional
from level2.dto import Task
from ..dto_advanced import (
    EffortForecastAdvancedConfig,
    TrendConfigAdvanced,
    RiskConfigAdvanced,
    DependencyConfigAdvanced,
    ForensicConfigAdvanced
)
from .effort_forecasting_advanced import EffortForecastingAdvancedAgent
from .trend_analysis_advanced import TrendAnalysisAdvancedAgent
from .risk_analysis_advanced import RiskAnalysisAdvancedAgent
from .dependency_mapping_advanced import DependencyMappingAdvancedAgent
from .forensic_analysis_advanced import ForensicAnalysisAdvancedAgent

class AnalyticsAggregator:
    name = "ANALYTICS_AGGREGATOR"

    def __init__(self):
        self.effort_agent = EffortForecastingAdvancedAgent()
        self.trend_agent = TrendAnalysisAdvancedAgent()
        self.risk_agent = RiskAnalysisAdvancedAgent()
        self.dependency_agent = DependencyMappingAdvancedAgent()
        self.forensic_agent = ForensicAnalysisAdvancedAgent()

    def run_all_analyses(self, task: Task, repo_fetcher=None) -> Dict[str, Any]:
        """
        Запускает все аналитические агенты на задаче и возвращает сводный отчет.
        """
        # Конфигурации по умолчанию
        effort_cfg = EffortForecastAdvancedConfig()
        trend_cfg = TrendConfigAdvanced()
        risk_cfg = RiskConfigAdvanced()
        dependency_cfg = DependencyConfigAdvanced()
        forensic_cfg = ForensicConfigAdvanced()

        # Запуск всех агентов
        effort_score, effort_details, effort_labels = self.effort_agent.score(task, effort_cfg)
        trend_score, trend_details, trend_labels = self.trend_agent.score(task, trend_cfg)
        risk_score, risk_details, risk_labels = self.risk_agent.score(task, risk_cfg)
        dependency_score, dependency_details, dependency_labels = self.dependency_agent.score(task, dependency_cfg, repo_fetcher)

        # Для Forensic Analysis нужен список задач
        # В этом примере используем только текущую задачу
        forensic_score, forensic_details, forensic_labels = self.forensic_agent.score([task], forensic_cfg)

        # Агрегация результатов
        result = {
            "effort": {
                "score": effort_score,
                "details": effort_details,
                "labels": effort_labels
            },
            "trend": {
                "score": trend_score,
                "details": trend_details,
                "labels": trend_labels
            },
            "risk": {
                "score": risk_score,
                "details": risk_details,
                "labels": risk_labels
            },
            "dependency": {
                "score": dependency_score,
                "details": dependency_details,
                "labels": dependency_labels
            },
            "forensic": {
                "score": forensic_score,
                "details": forensic_details,
                "labels": forensic_labels
            }
        }

        # Сводные метрики
        summary = self._generate_summary(result)

        return {
            "summary": summary,
            "details": result
        }

    def _generate_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерирует сводный отчет на основе результатов всех агентов.
        """
        # Средний риск
        avg_risk = result["risk"]["score"]

        # Тренд
        trend = result["trend"]["labels"].get("TREND", "FLAT")

        # Ожидаемые усилия
        expected_effort = result["effort"]["details"].get("expected_effort", 0)

        # Сложность зависимостей
        dependency_complexity = result["dependency"]["labels"].get("DEPENDENCY", "SIMPLE")

        # Рекомендации
        recommendations = []
        if avg_risk > 0.75:
            recommendations.append("Высокий риск — требуется внимание менеджера проекта.")
        if trend == "UP":
            recommendations.append("Тренд на увеличение усилий — пересмотрите оценки.")
        if dependency_complexity == "COMPLEX":
            recommendations.append("Сложные зависимости — упростите структуру задач.")

        summary = {
            "avg_risk": avg_risk,
            "trend": trend,
            "expected_effort": expected_effort,
            "dependency_complexity": dependency_complexity,
            "recommendations": recommendations
        }

        return summary

    def run_forensic_on_history(self, tasks_history: List[Task]) -> Dict[str, Any]:
        """
        Запускает только Forensic Analysis на истории задач.
        """
        forensic_cfg = ForensicConfigAdvanced()
        forensic_score, forensic_details, forensic_labels = self.forensic_agent.score(tasks_history, forensic_cfg)
        return {
            "score": forensic_score,
            "details": forensic_details,
            "labels": forensic_labels
        }











