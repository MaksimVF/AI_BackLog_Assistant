







from typing import Tuple, Dict, Any, List, Optional
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pydantic import BaseModel

# Импорт вашего Task DTO
from level2.dto import Task

from ..dto_advanced import EffortForecastAdvancedConfig
from ..utils import safe_float, moving_average

class EffortForecastingAdvancedAgent:
    name = "EFFORT_FORECAST_ADV"

    def _parse_history(self, task: Task) -> pd.Series:
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
            if all(x is not None for x in nums) and len(nums) > 0:
                # index as integer range
                s = pd.Series(nums, index=pd.RangeIndex(start=0, stop=len(nums)))
                return s
        except Exception:
            pass

        return pd.Series(dtype=float)

    def _pert_expected(self, meta: dict) -> Optional[float]:
        try:
            o = safe_float(meta.get("effort_o"), None)
            m = safe_float(meta.get("effort_m"), None)
            p = safe_float(meta.get("effort_p"), None)
            if m is not None:
                return (o + 4*m + p) / 6.0
        except Exception:
            return None
        return None

    def score(self, task: Task, cfg: EffortForecastAdvancedConfig) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, str]]:
        """
        Возвращает:
          forecast_details: {
            "method": str,
            "expected_effort": float,   # первая точка прогноза
            "forecast_series": [ {"ts": iso or idx, "mean":..., "ci_lower":..., "ci_upper":...}, ... ],
            "model": { diagnostics... }
          }
        internals: raw series, sma, ema, model objects (repr)
        labels: {"EFFORT_SRC": method}
        """
        meta = task.metadata or {}
        alpha = float(cfg.alpha)
        s = self._parse_history(task)

        # 1) сначала PERT (если есть и достаточно)
        pert = self._pert_expected(meta)
        if pert is not None and (len(s) < cfg.min_points):
            forecast_details = {
                "method": "PERT_FALLBACK",
                "expected_effort": float(pert),
                "forecast_series": [{"ts": None, "mean": float(pert), "ci_lower": float(pert), "ci_upper": float(pert)}],
                "model": {"note": "PERT used due to insufficient historical points"}
            }
            internals = {"source": "PERT", "pert": pert}
            return forecast_details, internals, {"EFFORT_SRC": "PERT"}

        n_points = len(s)
        internals: Dict[str, Any] = {"n_points": n_points}
        # compute SMA/EMA for diagnostics
        if cfg.use_ema and n_points > 0:
            try:
                ema = s.ewm(span=cfg.ema_span, adjust=False).mean()
                sma = s.rolling(window=min(cfg.ema_span, max(1, n_points))).mean()
                internals["ema_tail"] = ema.iloc[-3:].tolist() if len(ema) >= 3 else ema.tolist()
                internals["sma_tail"] = sma.iloc[-3:].tolist() if len(sma) >= 3 else sma.tolist()
            except Exception:
                internals["ema_tail"] = None
                internals["sma_tail"] = None

        # fallback if no data
        if n_points == 0:
            fallback = safe_float(task.effort, meta.get("effort", 1.0))
            forecast_details = {
                "method": "FALLBACK",
                "expected_effort": float(fallback),
                "forecast_series": [{"ts": None, "mean": float(fallback), "ci_lower": float(fallback), "ci_upper": float(fallback)}],
                "model": {"note": "no history; used fallback"}
            }
            return forecast_details, {"source": "FALLBACK"}, {"EFFORT_SRC": "FALLBACK"}

        # choose model: SARIMAX if requested & enough points, else OLS
        forecast_periods = int(cfg.forecast_periods)
        if cfg.use_sarimax and n_points >= max(cfg.min_points, 10):
            # prepare data as float array (index matters if time series)
            try:
                model = SARIMAX(s.values, order=cfg.sarimax_order, enforce_stationarity=False, enforce_invertibility=False)
                res = model.fit(disp=False)
                pred = res.get_forecast(steps=forecast_periods)
                mean = pred.predicted_mean
                ci = pred.conf_int(alpha=alpha)
                forecast_series = []
                # if time index exists
                if isinstance(s.index, pd.DatetimeIndex):
                    last_ts = s.index[-1]
                    for i in range(forecast_periods):
                        ts = (last_ts + pd.tseries.frequencies.to_offset(cfg.freq) * (i+1)).isoformat()
                        forecast_series.append({
                            "ts": ts,
                            "mean": float(mean[i]),
                            "ci_lower": float(ci.iloc[i, 0]),
                            "ci_upper": float(ci.iloc[i, 1])
                        })
                else:
                    for i in range(forecast_periods):
                        forecast_series.append({"ts": int(s.index[-1]) + i + 1, "mean": float(mean[i]), "ci_lower": float(ci.iloc[i,0]), "ci_upper": float(ci.iloc[i,1])})
                expected_effort = float(forecast_series[0]["mean"])
                model_info = {"aic": float(res.aic), "bic": float(res.bic), "method": "SARIMAX", "order": cfg.sarimax_order}
                forecast_details = {"method": "SARIMAX", "expected_effort": expected_effort, "forecast_series": forecast_series, "model": model_info}
                internals.update({"model_summary": res.summary().as_text()})
                return forecast_details, internals, {"EFFORT_SRC": "SARIMAX"}
            except Exception as e:
                # fallback to OLS if SARIMAX fails
                internals["sarimax_error"] = str(e)

        # OLS linear regression on index (works with datetime or integer index)
        try:
            if isinstance(s.index, pd.DatetimeIndex):
                # convert index to ordinal numbers (days)
                xs = np.array([(ts - s.index[0]).total_seconds() / 86400.0 for ts in s.index])
                last_x = xs[-1]
                future_x = np.array([last_x + (i+1) * (xs[1] - xs[0] if len(xs)>1 else 1.0) for i in range(forecast_periods)])
            else:
                xs = np.array(list(range(len(s))))
                last_x = xs[-1]
                future_x = np.array([last_x + (i+1) for i in range(forecast_periods)])

            X = sm.add_constant(xs)
            model = sm.OLS(s.values, X).fit()
            X_future = sm.add_constant(np.concatenate([xs, future_x]))
            pred = model.get_prediction(X_future)
            pred_df = pred.summary_frame(alpha=alpha)
            # separate forecast part
            forecast_series = []
            total_len = len(xs) + len(future_x)
            for i in range(len(xs), total_len):
                # timestamp for future point
                if isinstance(s.index, pd.DatetimeIndex):
                    # estimate time delta using median increment
                    if len(s.index) > 1:
                        delta = s.index[1] - s.index[0]
                    else:
                        delta = pd.Timedelta(1, unit=cfg.freq)
                    ts = (s.index[-1] + delta * (i - len(xs) + 1)).isoformat()
                else:
                    ts = i  # integer index
                mean = float(pred_df["mean"].iloc[i])
                ci_low = float(pred_df["mean_ci_lower"].iloc[i])
                ci_upp = float(pred_df["mean_ci_upper"].iloc[i])
                forecast_series.append({"ts": ts, "mean": mean, "ci_lower": ci_low, "ci_upper": ci_upp})
            expected_effort = float(forecast_series[0]["mean"])
            model_info = {"r2": float(model.rsquared), "aic": float(model.aic), "bic": float(model.bic), "method": "OLS"}
            forecast_details = {"method": "OLS", "expected_effort": expected_effort, "forecast_series": forecast_series, "model": model_info}
            internals.update({"ols_params": model.params.tolist(), "ols_summary": model.summary().as_text()})
            return forecast_details, internals, {"EFFORT_SRC": "OLS"}
        except Exception as e:
            # ultimate fallback
            fallback = safe_float(task.effort, meta.get("effort", 1.0))
            return {
                "method": "FALLBACK_AFTER_ERROR",
                "expected_effort": float(fallback),
                "forecast_series": [{"ts": None, "mean": float(fallback), "ci_lower": float(fallback), "ci_upper": float(fallback)}],
                "model": {"error": str(e)}
            }, {"error": str(e)}, {"EFFORT_SRC": "FALLBACK"}







