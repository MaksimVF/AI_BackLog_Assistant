



from typing import Tuple, Dict, Any, List, Set
import json
from level2.dto import Task, AnalysisConfig
from level2.scoring.base import BaseScoringAgent
from level2.scoring.utils import safe_float, clamp


class ImpactMappingAgent(BaseScoringAgent):
    name = "IMPACT_MAPPING"

    def _compute_direct_impact(self, targets: List[Any]) -> Tuple[float, Dict[str, Any]]:
        # targets может быть списком строк или dicts {"actor":"X","impact":0.8}
        total = 0.0
        details = {"actors": []}
        for t in targets or []:
            if isinstance(t, dict):
                actor = t.get("actor")
                impact = safe_float(t.get("impact"), 0.5)
            else:
                actor = str(t)
                impact = 0.5
            details["actors"].append({"actor": actor, "impact": impact})
            total += impact
        # нормируем по числу акторов
        score = total / max(len(details["actors"]), 1)
        return clamp(score, 0.0, 1.0), details

    def _compute_indirect_impact(self, task: Task, repo_fetcher, depth: int) -> Tuple[float, Dict[str, Any]]:
        """
        repo_fetcher: callable(task_id) -> Task OR None
        Это опционально: если есть возможность достать зависимые задачи, можно расширить влияние.
        В этой реализаии repo_fetcher может быть None -> возвращаем 0.
        """
        if repo_fetcher is None:
            return 0.0, {"indirect": "no_repo_fetcher"}
        visited: Set[str] = set()
        frontier = list(task.dependencies or [])
        level = 0
        indirect_score = 0.0
        details = {"indirect_contributions": []}
        while frontier and level < depth:
            next_frontier = []
            for tid in frontier:
                if tid in visited:
                    continue
                visited.add(tid)
                t = repo_fetcher(tid)
                if not t:
                    continue
                # берем влияние метаданных зависимой задачи (если есть)
                meta = t.metadata or {}
                contrib = safe_float(meta.get("impact_estimate"), 0.0)
                indirect_score += contrib * (0.5 ** level)  # уменьшающийся вес по глубине
                details["indirect_contributions"].append({"task_id": tid, "level": level, "contrib": contrib})
                # расширяем фронтир
                for d in t.dependencies or []:
                    if d not in visited:
                        next_frontier.append(d)
            frontier = next_frontier
            level += 1
        return clamp(indirect_score, 0.0, 1.0), details

    def score(self, task: Task, cfg: AnalysisConfig, repo_fetcher = None):
        """
        repo_fetcher: optional callable для получения задач по id
        """
        meta = task.metadata or {}


        targets_str = meta.get("impact_targets")

        # Parse JSON string
        try:
            targets = json.loads(targets_str) if targets_str else []
        except Exception:
            targets = []



        direct_score, direct_details = self._compute_direct_impact(targets)
        indirect_score, indirect_details = self._compute_indirect_impact(task, repo_fetcher, cfg.impact_mapping.depth)

        # комбинируем: даём больший вес прямому влиянию
        w_direct = 0.7
        w_indirect = 0.3
        final = clamp(w_direct * direct_score + w_indirect * indirect_score, 0.0, 1.0)

        details = {"direct": direct_details, "indirect": indirect_details, "w_direct": w_direct, "w_indirect": w_indirect}
        labels = {"IMPACT_BIN": "BROAD" if final >= 0.6 else "MEDIUM" if final >= 0.3 else "NARROW"}
        return float(final), details, labels


