









import pytest
from datetime import datetime, timedelta
from level2.analytics.agents_advanced.trend_analysis_advanced import TrendAnalysisAdvancedAgent
from level2.analytics.agents_advanced.risk_analysis_advanced import RiskAnalysisAdvancedAgent
from level2.analytics.agents_advanced.dependency_mapping_advanced import DependencyMappingAdvancedAgent
from level2.analytics.agents_advanced.forensic_analysis_advanced import ForensicAnalysisAdvancedAgent
from level2.analytics.dto_advanced import TrendConfigAdvanced, RiskConfigAdvanced, DependencyConfigAdvanced, ForensicConfigAdvanced
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

def test_trend_analysis_advanced():
    agent = TrendAnalysisAdvancedAgent()
    cfg = TrendConfigAdvanced(min_points=6, forecast_periods=2, use_exponential=True, use_sarima=False)
    t = make_task_with_history(8)
    score, details, labels = agent.score(t, cfg)
    assert "TREND" in labels
    assert score >= 0
    assert isinstance(details, dict)

def test_risk_analysis_advanced():
    agent = RiskAnalysisAdvancedAgent()
    cfg = RiskConfigAdvanced(use_ml=False)
    t = Task(id="T1", title="Test", metadata={"description": "High risk task", "risk_level": "HIGH"})
    score, details, labels = agent.score(t, cfg)
    assert "RISK_LEVEL" in labels
    assert score >= 0
    assert isinstance(details, dict)

def test_dependency_mapping_advanced():
    agent = DependencyMappingAdvancedAgent()
    cfg = DependencyConfigAdvanced(max_depth=2, visualize=False)
    t = Task(id="T1", title="Test", metadata={}, dependencies=["T2", "T3"])
    score, details, labels = agent.score(t, cfg, lambda x: Task(id=x, title="Test", metadata={}, dependencies=[]))
    assert "DEPENDENCY" in labels
    assert score >= 0
    assert isinstance(details, dict)

def test_forensic_analysis_advanced():
    agent = ForensicAnalysisAdvancedAgent()
    cfg = ForensicConfigAdvanced(delay_threshold_ratio=0.2, recurrence_threshold=3)
    tasks = [
        Task(id="T1", title="Test", metadata={"est_effort": 5, "actual_effort": 10, "delay_days": 5}),
        Task(id="T2", title="Test", metadata={"est_effort": 3, "actual_effort": 3, "delay_days": 0})
    ]
    score, details, labels = agent.score(tasks, cfg)
    assert "FORENSIC" in labels
    assert score >= 0
    assert isinstance(details, dict)









