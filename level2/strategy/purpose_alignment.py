


from typing import Tuple, Dict, Any, List
import json
from level2.dto import Task, AnalysisConfig
from level2.scoring.base import BaseScoringAgent
from level2.scoring.utils import safe_float, clamp


class PurposeAlignmentAgent(BaseScoringAgent):
    name = "PURPOSE_ALIGNMENT"

    def _score_by_overlap(self, task_goals: List[str], project_goals: Dict[str, float]) -> Tuple[float, Dict[str, Any]]:
        """
        Простая мера: количество пересекающихся целей / суммарный вес целей проекта.
        project_goals: {"okr1": weight, "okr2": weight}
        """
        if not project_goals:
            return 0.0, {"reason": "no_project_goals"}

        matched_weights = 0.0
        total_weights = sum(project_goals.values()) if project_goals else 0.0
        matched = []
        for g in task_goals or []:
            g_norm = g.strip().lower()
            for okr, w in project_goals.items():
                if g_norm in okr.lower() or okr.lower() in g_norm:
                    matched_weights += safe_float(w, 0.0)
                    matched.append(okr)
        score = (matched_weights / total_weights) if total_weights > 0 else 0.0
        return clamp(score, 0.0, 1.0), {"matched_goals": matched, "matched_weight": matched_weights, "total_weight": total_weights}

    def score(self, task: Task, cfg: AnalysisConfig):
        meta = task.metadata or {}
        # Parse JSON strings from metadata
        task_goals_str = meta.get("goals")
        project_goals_str = meta.get("project_goals") or meta.get("okrs")

        try:
            task_goals = json.loads(task_goals_str) if task_goals_str else []
        except Exception:
            task_goals = []

        try:
            project_goals = json.loads(project_goals_str) if project_goals_str else {}
        except Exception:
            project_goals = {}

        raw_score, details = self._score_by_overlap(task_goals, project_goals)

        # интерпретация
        aligned = "aligned" if raw_score >= cfg.purpose_alignment.aligned_threshold else "misaligned"

        details.update({
            "task_goals": task_goals,
            "project_goals_count": len(project_goals) if hasattr(project_goals, "keys") else 0
        })
        labels = {"PURPOSE": aligned}
        # итоговый score учитывает вес goal_weight
        score = raw_score * safe_float(cfg.purpose_alignment.goal_weight, 1.0)
        return float(score), details, labels

