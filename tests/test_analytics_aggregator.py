











import pytest
from datetime import datetime, timedelta
from level2.analytics.agents_advanced.analytics_aggregator import AnalyticsAggregator
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

def test_analytics_aggregator():
    aggregator = AnalyticsAggregator()
    t = make_task_with_history(8)
    result = aggregator.run_all_analyses(t)
    assert "summary" in result
    assert "details" in result
    assert "avg_risk" in result["summary"]
    assert "trend" in result["summary"]
    assert "expected_effort" in result["summary"]
    assert "dependency_complexity" in result["summary"]
    assert "recommendations" in result["summary"]

def test_forensic_analysis_only():
    aggregator = AnalyticsAggregator()
    t = make_task_with_history(8)
    result = aggregator.run_forensic_on_history([t])
    assert "score" in result
    assert "details" in result
    assert "labels" in result

def test_aggregator_with_empty_task():
    aggregator = AnalyticsAggregator()
    t = Task(id="T1", title="Test", metadata={})
    result = aggregator.run_all_analyses(t)
    assert "summary" in result
    assert "details" in result
    assert isinstance(result["summary"], dict)
    assert isinstance(result["details"], dict)











