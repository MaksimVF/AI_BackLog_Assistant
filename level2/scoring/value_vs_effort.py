

from typing import Dict, Tuple
from level2.dto import Task, AnalysisConfig

class ValueVsEffortAgent:
    """
    Агент для матричного анализа Value vs Effort.
    Идея: высокая ценность при низких усилиях = top priority.
    """
    name = "VALUE_EFFORT"

    def score(self, task: Task, config: AnalysisConfig) -> Tuple[float, Dict, Dict]:
        value = float(task.metadata.get("value", 5))   # 0–10
        effort = float(task.effort or task.metadata.get("effort", 5))  # 0–10

        if effort <= 0:
            effort = 1.0

        raw_score = value / effort

        # нормируем к 0–10
        score = min(raw_score * 2, 10.0)

        labels = {"VALUE_EFFORT_BIN": "HIGH" if score >= 7 else "MEDIUM" if score >= 4 else "LOW"}

        details = {
            "value": value,
            "effort": effort,
            "ratio": raw_score,
            "final_score": score
        }
        return score, details, labels

