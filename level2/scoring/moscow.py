



from .base import BaseScoringAgent
from ..dto import Task, AnalysisConfig
from .utils import safe_float, clamp

class MoSCoWAgent(BaseScoringAgent):
    """
    Базовая маркировка: must/should/could/wont (из meta['moscow'] или правил).
    Численный score = base_weight + adjustments:
      + dependency_boost (если есть critical_dependency=1)
      + deadline_boost (если deadline_days <= threshold)
      - capacity_penalty (если sprint_capacity_deficit=1)
    """
    name = "MOSCOW"

    def score(self, task: Task, cfg: AnalysisConfig):
        meta = task.metadata or {}
        label = (meta.get("moscow") or "could").lower()
        base_w = cfg.moscow.base_weights.get(label, 0.5)

        # корректировки
        dep_boost = cfg.moscow.dependency_boost if safe_float(meta.get("critical_dependency"), 0.0) >= 1.0 else 0.0

        deadline_days = safe_float(meta.get("deadline_days"), 9999.0)
        dl_boost = cfg.moscow.deadline_boost if deadline_days <= cfg.moscow.deadline_days_threshold else 0.0

        cap_penalty = cfg.moscow.capacity_penalty if safe_float(meta.get("sprint_capacity_deficit"), 0.0) >= 1.0 else 0.0

        score = clamp(base_w + dep_boost + dl_boost - cap_penalty, 0.0, 1.2)

        details = {
            "label": label,
            "base_weight": base_w,
            "dependency_boost": dep_boost,
            "deadline_boost": dl_boost,
            "capacity_penalty": cap_penalty,
            "deadline_days": deadline_days,
        }
        labels = {"MOSCOW": label}
        return score, details, labels



