









from typing import Tuple, Dict, Any, List, Callable
from level2.dto import Task
from ..dto import EffortForecastConfig
from ..utils import moving_average, linear_regression, safe_float
import statistics, math

class EffortForecastingAgent:
    name = "EFFORT_FORECAST"

    def _pert_expected(self, meta):
        # ищем effort_o/_m/_p
        try:
            o = safe_float(meta.get("effort_o"), None)
            m = safe_float(meta.get("effort_m"), None)
            p = safe_float(meta.get("effort_p"), None)
            if m and p is not None:
                # PERT mean
                return (o + 4*m + p) / 6.0
        except Exception:
            pass
        return None

    def score(self, task: Task, cfg: EffortForecastConfig, repo_fetcher: Callable[[str], Task] = None) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        """
        Возвращает (forecast_details, internals, labels)
        forecast_details: {"expected_effort": float, "variance": float}
        internals: дополнительные данные для аудита
        """
        meta = task.metadata or {}
        history_efforts = meta.get("history_efforts") or []  # list of floats
        # если есть PERT, используем его как главный источник
        pert = self._pert_expected(meta)
        if pert is not None:
            expected = pert
            variance = ((safe_float(meta.get("effort_p"), pert) - safe_float(meta.get("effort_o"), pert)) / 6.0) ** 2 if meta.get("effort_p") else 0.0
            internals = {"method": "PERT", "pert": pert}
            labels = {"EFFORT_SRC": "PERT"}
            return {"expected_effort": float(expected), "variance": float(variance)}, internals, labels

        # иначе используем исторические данные (из текущ задачи/проекта)
        hist = [safe_float(x) for x in history_efforts if safe_float(x, None) is not None]
        if repo_fetcher and cfg.history_size and not hist:
            # попытка собрать похожие задачи: repo_fetcher может вернуть list? Здесь предполагаем repo_fetcher(task_id) только
            pass

        if len(hist) >= cfg.min_points:
            # простой прогноз: взвешенное среднее последних N значений + SMA
            window = min(3, len(hist))
            ma = moving_average(hist, window)[-1]
            expected = ma
            variance = statistics.pvariance(hist) if len(hist) > 1 else 0.0
            internals = {"method": "HIST_MA", "history": hist, "window": window}
            labels = {"EFFORT_SRC": "HISTORY"}
            return {"expected_effort": float(expected), "variance": float(variance)}, internals, labels

        # fallback: используем task.effort если задан, либо default 1.0
        fallback = safe_float(task.effort, safe_float(meta.get("effort"), 1.0))
        internals = {"method": "FALLBACK", "fallback": fallback}
        labels = {"EFFORT_SRC": "FALLBACK"}
        return {"expected_effort": float(fallback), "variance": 0.0}, internals, labels









