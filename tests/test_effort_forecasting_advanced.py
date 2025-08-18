








import pytest
from datetime import datetime, timedelta
from level2.analytics.agents.effort_forecasting_advanced import EffortForecastingAdvancedAgent
from level2.analytics.dto_advanced import EffortForecastAdvancedConfig
from level2.dto import Task

def make_task_with_history(n=10, start=None):
    if start is None:
        start = datetime.utcnow() - timedelta(days=n)
    hist = []
    for i in range(n):
        ts = (start + timedelta(days=i)).isoformat()
        # простая возрастающая история усилий
        hist.append({"ts": ts, "effort": 2.0 + i*0.5})
    t = Task(id="T1", title="Test", metadata={"history_efforts": hist})
    return t

def test_ols_forecast():
    agent = EffortForecastingAdvancedAgent()
    cfg = EffortForecastAdvancedConfig(min_points=6, forecast_periods=2, use_ema=True, use_ols=True, use_sarimax=False)
    t = make_task_with_history(8)
    forecast, internals, labels = agent.score(t, cfg)
    assert "method" in forecast
    assert forecast["method"] in ("OLS",)
    assert forecast["expected_effort"] > 0
    assert isinstance(forecast["forecast_series"], list)
    assert labels["EFFORT_SRC"] == forecast["method"]

def test_sarimax_fallback_to_ols_if_disabled():
    agent = EffortForecastingAdvancedAgent()
    cfg = EffortForecastAdvancedConfig(min_points=6, forecast_periods=1, use_sarimax=False)
    t = make_task_with_history(7)
    forecast, internals, labels = agent.score(t, cfg)
    assert forecast["method"] in ("OLS",)

def test_pert_fallback():
    agent = EffortForecastingAdvancedAgent()
    t = Task(id="T1", title="Test", metadata={"effort_o": 1, "effort_m": 2, "effort_p": 3})
    cfg = EffortForecastAdvancedConfig(min_points=6, forecast_periods=1)
    forecast, internals, labels = agent.score(t, cfg)
    assert forecast["method"] == "PERT_FALLBACK"
    assert forecast["expected_effort"] == (1 + 4*2 + 3) / 6.0

def test_no_data_fallback():
    agent = EffortForecastingAdvancedAgent()
    t = Task(id="T1", title="Test", metadata={}, effort=5.0)
    cfg = EffortForecastAdvancedConfig(min_points=6, forecast_periods=1)
    forecast, internals, labels = agent.score(t, cfg)
    assert forecast["method"] == "FALLBACK"
    assert forecast["expected_effort"] == 5.0

def test_insufficient_data_fallback():
    agent = EffortForecastingAdvancedAgent()
    t = Task(id="T1", title="Test", metadata={"history_efforts": [1, 2, 3]}, effort=5.0)
    cfg = EffortForecastAdvancedConfig(min_points=6, forecast_periods=1)
    forecast, internals, labels = agent.score(t, cfg)
    assert forecast["method"] == "FALLBACK"
    assert forecast["expected_effort"] == 5.0







