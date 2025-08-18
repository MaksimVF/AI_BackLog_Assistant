








import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from typing import Dict, Any, Tuple
from level2.dto import Task
from ..dto_advanced import TrendConfigAdvanced
from ..utils import safe_float

class TrendAnalysisAdvancedAgent:
    name = "TREND_ANALYSIS_ADV"

    def _parse_series(self, task: Task) -> pd.Series:
        """
        Поддерживает разные форматы в task.metadata:
         - metadata["history_efforts"] = [{"ts": ISO, "effort": num}, ...]
         - metadata["history_efforts"] = [num, num, ...]  (в этом случае создаём индекс 0..n-1)
         - metadata["history"] = [{"ts":..., "value":...}, ...] (backwards compatible)
         - PERT: effort_o/_m/_p handled отдельно
        Возвращает pandas.Series indexed by datetime (если есть даты) или by integer index.
        """
        meta = task.metadata or {}
        hist = meta.get("history_efforts") or meta.get("history") or []
        # detect format
        if not hist:
            return pd.Series(dtype=float)

        # if list of dicts with 'ts' and 'effort' or 'value'
        if isinstance(hist, list) and len(hist) and isinstance(hist[0], dict) and ("ts" in hist[0] or "date" in hist[0]):
            rows = []
            for it in hist:
                ts = it.get("ts") or it.get("date")
                try:
                    idx = pd.to_datetime(ts)
                except Exception:
                    continue
                val = safe_float(it.get("effort") if "effort" in it else it.get("value"), None)
                if val is None:
                    continue
                rows.append((idx, val))
            if not rows:
                return pd.Series(dtype=float)
            s = pd.Series([r[1] for r in rows], index=[r[0] for r in rows]).sort_index()
            return s

        # if list of tuples / lists like [ [ts, value], ... ]
        if isinstance(hist, list) and len(hist) and isinstance(hist[0], (list, tuple)) and len(hist[0]) >= 2:
            rows = []
            for it in hist:
                try:
                    idx = pd.to_datetime(it[0])
                    val = safe_float(it[1], None)
                    if val is None:
                        continue
                    rows.append((idx, val))
                except Exception:
                    continue
            if rows:
                s = pd.Series([r[1] for r in rows], index=[r[0] for r in rows]).sort_index()
                return s

        # if it's just a list of numbers
        try:
            nums = [safe_float(x) for x in hist]
            if nums and all(x is not None for x in nums):
                s = pd.Series(nums, index=pd.RangeIndex(start=0, stop=len(nums)))
                return s
        except Exception:
            pass

        return pd.Series(dtype=float)

    def score(self, task: Task, cfg: TrendConfigAdvanced) -> Tuple[float, Dict[str, Any], Dict[str, str]]:
        s = self._parse_series(task)
        if len(s) < cfg.min_points:
            return 0.0, {"reason": "insufficient_points"}, {"TREND": "FLAT"}

        # Попробуем несколько моделей
        models = []

        # Линейная регрессия
        try:
            X = np.arange(len(s))
            X = sm.add_constant(X)
            model = sm.OLS(s.values, X).fit()
            models.append({"model": model, "type": "linear", "aic": model.aic})
        except:
            pass

        # Экспоненциальное сглаживание
        if cfg.use_exponential:
            try:
                model = ExponentialSmoothing(s, trend="add", seasonal=None).fit()
                models.append({"model": model, "type": "exp", "aic": model.aic})
            except:
                pass

        # SARIMA (если достаточно данных)
        if cfg.use_sarima and len(s) >= 10:
            try:
                model = SARIMAX(s, order=cfg.sarima_order, seasonal_order=(0,0,0,0)).fit(disp=False)
                models.append({"model": model, "type": "sarima", "aic": model.aic})
            except:
                pass

        if not models:
            return 0.0, {"reason": "no_model_fitted"}, {"TREND": "FLAT"}

        # Выбираем лучшую модель по AIC
        best = min(models, key=lambda x: x["aic"])
        trend_type = best["type"]

        # Прогноз
        forecast = best["model"].forecast(steps=cfg.forecast_periods)
        details = {
            "model": trend_type,
            "aic": best["aic"],
            "forecast": forecast.tolist()
        }

        # Определяем направление тренда
        if trend_type == "linear":
            direction = "UP" if best["model"].params[1] > 0 else "DOWN" if best["model"].params[1] < 0 else "FLAT"
        else:
            direction = "UP" if forecast[-1] > s.iloc[-1] else "DOWN" if forecast[-1] < s.iloc[-1] else "FLAT"

        return 1.0, details, {"TREND": direction}








