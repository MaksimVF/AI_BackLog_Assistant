



from typing import Tuple, Dict, Any
from level2.dto import Task, AnalysisConfig
from level2.scoring.base import BaseScoringAgent
from level2.scoring.utils import safe_float, clamp, normalize01
import math

class CostOfDelayAgent(BaseScoringAgent):
    name = "COST_OF_DELAY"

    def score(self, task: Task, cfg: AnalysisConfig):
        meta = task.metadata or {}
        # value per day:
        vpd = safe_float(meta.get(cfg.cost_of_delay.value_per_time_unit_key), cfg.cost_of_delay.default_value_per_day)
        # urgency: если есть deadline_days -> higher urgency for smaller days
        deadline_days = safe_float(meta.get("deadline_days"), None)
        if deadline_days is None or deadline_days <= 0:
            urgency = safe_float(meta.get("urgency_factor"), 0.5)
        else:
            # простая шкала: 0 days -> 1.0; 90+ days -> 0.0
            urgency = clamp((90.0 - clamp(deadline_days, 0.0, 90.0)) / 90.0, 0.0, 1.0)

        cod_raw = vpd * urgency  # экономический убыток в денежной единице в день (условно)
        # нормализуем к 0..1 по cfg.cod_min/cod_max
        cod_norm = normalize01(cod_raw, cfg.cost_of_delay.cod_min, cfg.cost_of_delay.cod_max)

        details = {"value_per_day": vpd, "urgency": urgency, "cod_raw": cod_raw, "cod_norm": cod_norm, "deadline_days": deadline_days}
        labels = {"CoD_BIN": "CRITICAL" if cod_norm >= 0.75 else "HIGH" if cod_norm>=0.5 else "MODERATE" if cod_norm>=0.25 else "LOW"}
        # Для приоритизации — чем выше CoD, тем выше priority => score = cod_norm
        return float(cod_norm), details, labels



