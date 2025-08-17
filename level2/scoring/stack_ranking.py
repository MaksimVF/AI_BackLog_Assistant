
from typing import Dict, Tuple
from level2.dto import Task, AnalysisConfig

class StackRankingAgent:
    """
    Агент для упорядочивания задач по пользовательскому приоритету.
    Основа — явные приоритеты (0–100) или голосование стейкхолдеров.
    """

    def score(self, task: Task, config: AnalysisConfig) -> Tuple[float, Dict, Dict]:
        base_priority = float(task.metadata.get("priority", 50))  # дефолт 50
        votes_str = task.metadata.get("votes", "")  # строка чисел через запятую

        if votes_str:
            try:
                votes = [float(v) for v in votes_str.split(",")]
                avg_vote = sum(votes) / len(votes)
            except (ValueError, ZeroDivisionError):
                avg_vote = base_priority
        else:
            avg_vote = base_priority

        # нормируем в 0–10
        score = avg_vote / 10.0
        labels = {"STACK_BIN": "HIGH" if score >= 7 else "MEDIUM" if score >= 4 else "LOW"}

        details = {
            "base_priority": base_priority,
            "avg_vote": avg_vote,
            "final_score": score
        }
        return score, details, labels
