







from typing import Tuple, Dict, Any
from ..dto import RiskConfig
from ..utils import safe_float
from level2.dto import Task
import math

class RiskAnalysisAgent:
    name = "RISK_ANALYSIS"

    def score(self, task: Task, cfg: RiskConfig) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        meta = task.metadata or {}
        prob = safe_float(meta.get("risk_prob"), None)
        impact = safe_float(meta.get("risk_impact"), None)
        hist_failures = int(meta.get("historical_failures", 0))
        dependency_count = int(len(task.dependencies or []))

        # если явно заданы prob/impact используем их
        if prob is not None and impact is not None:
            base_risk = prob * impact
        else:
            # эвристика: derive from historical_failures and flags
            base_risk = min(1.0, 0.1 * hist_failures + 0.05 * dependency_count)

        # добавим вклад исторических отказов (нормируем)
        hist_factor = min(1.0, hist_failures / 10.0)
        dep_factor = min(1.0, dependency_count / 10.0)

        combined = (cfg.failure_weight * hist_factor) + (cfg.dependency_weight * dep_factor) + (cfg.metadata_risk_weight * base_risk)
        score = min(1.0, combined)

        details = {
            "prob": prob,
            "impact": impact,
            "historical_failures": hist_failures,
            "dependency_count": dependency_count,
            "base_risk": base_risk,
            "hist_factor": hist_factor,
            "dep_factor": dep_factor,
            "combined_raw": combined
        }

        label = "CRITICAL" if score >= 0.75 else "HIGH" if score >= 0.5 else "MEDIUM" if score >= 0.2 else "LOW"
        return float(score), details, {"RISK_LEVEL": label}






