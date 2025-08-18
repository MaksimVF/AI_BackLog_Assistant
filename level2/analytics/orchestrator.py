








from typing import Dict, Any, Callable, List, Tuple
from level2.dto import Task
from .agents.trend_analysis import TrendAnalysisAgent
from .agents.risk_analysis import RiskAnalysisAgent
from .agents.dependency_mapping import DependencyMappingAgent
from .agents.effort_forecasting import EffortForecastingAgent
from .agents.forensic_analysis import ForensicAnalysisAgent
from .dto import TrendConfig, RiskConfig, DependencyConfig, EffortForecastConfig, ForensicConfig

class AnalyticsOrchestrator:
    def __init__(self):
        self.agents = {
            "trend": TrendAnalysisAgent(),
            "risk": RiskAnalysisAgent(),
            "dependency": DependencyMappingAgent(),
            "effort": EffortForecastingAgent(),
            "forensic": ForensicAnalysisAgent()
        }

    def run_trend_analysis(self, task: Task, cfg: TrendConfig) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        return self.agents["trend"].score(task, cfg)

    def run_risk_analysis(self, task: Task, cfg: RiskConfig) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        return self.agents["risk"].score(task, cfg)

    def run_dependency_analysis(self, task: Task, cfg: DependencyConfig, repo_fetcher: Callable[[str], Task] = None) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        return self.agents["dependency"].score(task, cfg, repo_fetcher)

    def run_effort_forecast(self, task: Task, cfg: EffortForecastConfig, repo_fetcher: Callable[[str], Task] = None) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        return self.agents["effort"].score(task, cfg, repo_fetcher)

    def run_forensic_analysis(self, tasks_history: List[Task], cfg: ForensicConfig, repo_fetcher: Callable[[str], Task] = None) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        return self.agents["forensic"].score(tasks_history, cfg, repo_fetcher)

    def run_all_analyses(self, task: Task, tasks_history: List[Task] = None, repo_fetcher: Callable[[str], Task] = None) -> Dict[str, Any]:
        """
        Запускает все анализы для задачи и возвращает агрегированный результат.
        """
        results = {}
        # Trend
        trend_score, trend_details, trend_labels = self.run_trend_analysis(task, TrendConfig())
        results["trend"] = {"score": trend_score, "details": trend_details, "labels": trend_labels}

        # Risk
        risk_score, risk_details, risk_labels = self.run_risk_analysis(task, RiskConfig())
        results["risk"] = {"score": risk_score, "details": risk_details, "labels": risk_labels}

        # Dependency
        dep_score, dep_details, dep_labels = self.run_dependency_analysis(task, DependencyConfig(), repo_fetcher)
        results["dependency"] = {"score": dep_score, "details": dep_details, "labels": dep_labels}

        # Effort
        effort_forecast, effort_details, effort_labels = self.run_effort_forecast(task, EffortForecastConfig(), repo_fetcher)
        results["effort"] = {"forecast": effort_forecast, "details": effort_details, "labels": effort_labels}

        # Forensic (если есть история)
        if tasks_history:
            forensic_score, forensic_details, forensic_labels = self.run_forensic_analysis(tasks_history, ForensicConfig())
            results["forensic"] = {"score": forensic_score, "details": forensic_details, "labels": forensic_labels}

        return results










