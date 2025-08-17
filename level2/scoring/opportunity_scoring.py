


from typing import Dict, Tuple
from level2.dto import Task, AnalysisConfig

class OpportunityScoringAgent:
    """
    Агент для Opportunity Scoring:
    – Оценивает фичу по двум осям: Importance (важность) и Satisfaction (удовлетворённость текущим решением).
    – Приоритет = Importance - Satisfaction.
    """
    name = "OPPORTUNITY"

    def score(self, task: Task, config: AnalysisConfig) -> Tuple[float, Dict, Dict]:
        importance = float(task.metadata.get("importance", 5))     # 0–10
        satisfaction = float(task.metadata.get("satisfaction", 5)) # 0–10

        raw_score = importance - satisfaction
        score = max(0.0, raw_score)  # отрицательные не даём
        score = min(score, 10.0)

        labels = {
            "OPPORTUNITY_BIN": "HIGH" if score >= 7 else "MEDIUM" if score >= 4 else "LOW"
        }

        details = {
            "importance": importance,
            "satisfaction": satisfaction,
            "gap": raw_score,
            "final_score": score
        }
        return score, details, labels


