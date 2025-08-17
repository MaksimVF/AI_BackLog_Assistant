




from typing import Tuple, Dict, Any
from level2.dto import Task, AnalysisConfig
from level2.scoring.base import BaseScoringAgent
from level2.scoring.utils import safe_float, clamp, normalize01

class RoiAgent(BaseScoringAgent):
    name = "ROI"

    def score(self, task: Task, cfg: AnalysisConfig):
        meta = task.metadata or {}
        # expected_gain: общий выгодный эффект
        expected_gain = safe_float(meta.get("expected_gain"), cfg.roi.default_gain)
        # cost: затраты на реализацию
        cost = safe_float(meta.get("cost"), cfg.roi.default_cost)
        # horizon: временной горизонт для расчёта ROI
        horizon_days = safe_float(meta.get("horizon_days"), cfg.roi.horizon_days)

        # ROI = (expected_gain - cost) / cost
        if cost <= 0:
            roi_raw = 0.0
        else:
            roi_raw = (expected_gain - cost) / cost

        # нормализуем к 0..1
        roi_norm = normalize01(roi_raw, -1.0, 10.0)  # -100% до 1000% ROI

        details = {
            "expected_gain": expected_gain,
            "cost": cost,
            "horizon_days": horizon_days,
            "roi_raw": roi_raw,
            "roi_norm": roi_norm
        }
        labels = {"ROI_BIN": "HIGH" if roi_norm >= 0.75 else "MEDIUM" if roi_norm >= 0.25 else "LOW"}
        return float(roi_norm), details, labels




