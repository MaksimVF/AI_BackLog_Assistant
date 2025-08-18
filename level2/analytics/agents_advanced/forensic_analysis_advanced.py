










import pandas as pd
from typing import Dict, Any, Tuple
from level2.dto import Task
from ..dto_advanced import ForensicConfigAdvanced
from ..utils import safe_float

class ForensicAnalysisAdvancedAgent:
    name = "FORENSIC_ANALYSIS_ADV"

    def score(self, tasks_history: list, cfg: ForensicConfigAdvanced) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        # Анализ истории задач
        data = []
        for t in tasks_history:
            meta = t.metadata or {}
            data.append({
                "task_id": t.id,
                "est_effort": safe_float(meta.get("est_effort", 0)),
                "actual_effort": safe_float(meta.get("actual_effort", 0)),
                "delay": safe_float(meta.get("delay_days", 0)),
                "blockers": meta.get("blockers", [])
            })

        df = pd.DataFrame(data)

        # Анализ задержек
        df["delay_ratio"] = df["delay"] / df["est_effort"]
        high_delay = df[df["delay_ratio"] > cfg.delay_threshold_ratio]

        # Анализ блокировщиков
        blockers = df["blockers"].explode().value_counts()

        details = {
            "high_delay_tasks": high_delay.to_dict(orient="records"),
            "common_blockers": blockers.to_dict()
        }

        # Оценка проблемности
        severity = len(high_delay) / len(df)

        return severity, details, {"FORENSIC": "CRITICAL" if severity > 0.5 else "OK"}










