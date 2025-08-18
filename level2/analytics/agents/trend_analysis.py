






from typing import Tuple, Dict, Any, List
from ..dto import TrendConfig
from ..utils import linear_regression, safe_float
from level2.dto import Task
import datetime

class TrendAnalysisAgent:
    name = "TREND_ANALYSIS"

    def _parse_series(self, raw: List) -> Tuple[List[float], List[float]]:
        """
        raw: list of {"ts": iso_str, "value": number} OR list of [ts_iso, value].
        Возвращает xs (days since epoch), ys (values)
        """
        xs = []
        ys = []
        for item in raw or []:
            try:
                if isinstance(item, dict):
                    ts = item.get("ts")
                    val = safe_float(item.get("value"))
                elif isinstance(item, (list, tuple)):
                    ts, val = item[0], item[1]
                    val = safe_float(val)
                else:
                    continue
                dt = datetime.datetime.fromisoformat(ts)
                xs.append(dt.timestamp() / 86400.0)  # дни
                ys.append(val)
            except Exception:
                continue
        return xs, ys

    def score(self, task: Task, cfg: TrendConfig) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        meta = task.metadata or {}
        raw = meta.get("history") or []
        xs, ys = self._parse_series(raw)
        details = {"n_points": len(xs)}
        if len(xs) < cfg.min_points:
            return 0.0, {**details, "reason": "insufficient_points"}, {"TREND": "FLAT"}

        a, b = linear_regression(xs, ys)
        # b — изменение в value per day; силу нормируем через среднее abs(y)
        avg_y = sum(abs(v) for v in ys) / len(ys) if ys else 0.0
        strength = 0.0
        if avg_y > 1e-6:
            strength = min(1.0, abs(b) * 30.0 / avg_y)  # эвристическая нормализация (30 дней scale)
        direction = "UP" if b > 0 else "DOWN" if b < 0 else "FLAT"
        score = strength
        details.update({"a": a, "b": b, "avg_y": avg_y, "direction": direction})
        labels = {"TREND": direction}
        return float(score), details, labels






