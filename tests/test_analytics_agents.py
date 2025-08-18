







import pytest
from level2.dto import Task
from level2.analytics.agents.trend_analysis import TrendAnalysisAgent
from level2.analytics.agents.risk_analysis import RiskAnalysisAgent
from level2.analytics.agents.dependency_mapping import DependencyMappingAgent
from level2.analytics.agents.effort_forecasting import EffortForecastingAgent
from level2.analytics.agents.forensic_analysis import ForensicAnalysisAgent
from level2.analytics.dto import TrendConfig, RiskConfig, DependencyConfig, EffortForecastConfig, ForensicConfig

def make_task(id="t1", metadata=None, dependencies=None, effort=None):
    return Task(id=id, title="t", description=None, tags=[], effort=effort, reach=None, impact=None, confidence=None, dependencies=dependencies or [], created_at=None, metadata=metadata or {})

def test_trend_analysis_basic():
    agent = TrendAnalysisAgent()
    # строим простую серию: день 1 -> 10, день 2 -> 12, day3 -> 15
    from datetime import datetime, timedelta
    base = datetime.utcnow()
    hist = []
    for i, v in enumerate([10, 12, 15]):
        ts = (base - timedelta(days=3-i)).isoformat()
        hist.append({"ts": ts, "value": v})
    t = make_task(metadata={"history": hist})
    score, details, labels = agent.score(t, TrendConfig(window_days=30, min_points=3))
    assert 0.0 <= score <= 1.0
    assert labels["TREND"] in ("UP","DOWN","FLAT")

def test_risk_analysis_basic():
    agent = RiskAnalysisAgent()
    t = make_task(metadata={"risk_prob": 0.4, "risk_impact": 0.7, "historical_failures": 2}, dependencies=["d1"])
    score, details, labels = agent.score(t, RiskConfig())
    assert 0.0 <= score <= 1.0
    assert "RISK_LEVEL" in labels

def test_dependency_mapping_cycle_and_critical():
    agent = DependencyMappingAgent()
    # mock repo_fetcher
    tasks = {
        "A": make_task(id="A", dependencies=["B"], effort=3),
        "B": make_task(id="B", dependencies=["C"], effort=2),
        "C": make_task(id="C", dependencies=[], effort=5),
    }
    def fetch(tid):
        return tasks.get(tid)
    root = tasks["A"]
    score, details, labels = agent.score(root, DependencyConfig(max_depth=5), repo_fetcher=fetch)
    assert "nodes_count" in details
    # without cycles -> label != "CYCLE"
    assert labels["DEP_LABEL"] != "CYCLE"

def test_effort_forecasting_hist():
    agent = EffortForecastingAgent()
    t = make_task(metadata={"history_efforts":[3,4,5]})
    forecast, internals, labels = agent.score(t, EffortForecastConfig(history_size=10, min_points=2))
    assert "expected_effort" in forecast
    assert forecast["expected_effort"] > 0

def test_forensic_basic():
    agent = ForensicAnalysisAgent()
    tasks = [
        make_task(id="x1", metadata={"est_effort":2,"actual_effort":4,"blockers":["dep"], "delay_days":3}),
        make_task(id="x2", metadata={"est_effort":5,"actual_effort":5,"blockers":[]}),
        make_task(id="x3", metadata={"est_effort":3,"actual_effort":6,"blockers":["dep"], "resource_issue": True}),
    ]
    score, details, labels = agent.score(tasks, ForensicConfig(delay_threshold_ratio=0.2, recurrence_threshold=2))
    assert 0.0 <= score <= 1.0
    assert "recommendations" in details






