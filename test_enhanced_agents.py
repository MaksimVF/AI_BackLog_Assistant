


import pytest
from level2.dto import Task, AnalysisConfig
from level2.scoring.rice import RiceAgent
from level2.scoring.wsjf import WSJFAgent
from level2.scoring.kano import KanoAgent
from level2.scoring.moscow import MoSCoWAgent
from datetime import datetime

def test_rice_basic():
    agent = RiceAgent()
    task = Task(
        id="1",
        title="Test RICE",
        reach=5000,
        impact=2.0,
        confidence=0.8,
        effort=5,
        created_at=datetime.now()
    )
    cfg = AnalysisConfig()
    score, details, labels = agent.score(task, cfg)
    assert score > 0
    assert "reach_norm" in details
    assert labels["RICE_BIN"] in ["HIGH", "MEDIUM", "LOW"]

def test_rice_with_risk():
    agent = RiceAgent()
    task = Task(
        id="2",
        title="Risky task",
        reach=1000,
        impact=1.0,
        confidence=0.9,
        effort=2,
        metadata={"risk_prob": 0.5, "risk_impact": 0.8},
        created_at=datetime.now()
    )
    cfg = AnalysisConfig()
    cfg.rice.risk_penalty = 0.5
    score, details, _ = agent.score(task, cfg)
    assert score < details["base_rice"]

def test_wsjf_basic():
    agent = WSJFAgent()
    task = Task(
        id="3",
        title="WSJF case",
        effort=3,
        metadata={"bv": 8, "tc": 5, "rr_oe": 3},
        created_at=datetime.now()
    )
    cfg = AnalysisConfig()
    score, details, labels = agent.score(task, cfg)
    assert score > 0
    assert "BV" in details
    assert labels["WSJF_BIN"] in ["HIGH", "MEDIUM", "LOW"]

def test_kano_votes():
    agent = KanoAgent()
    task = Task(
        id="4",
        title="Kano survey",
        metadata={"kano_votes": [(1,2), (1,3), (2,5)]},
        created_at=datetime.now()
    )
    cfg = AnalysisConfig()
    score, details, labels = agent.score(task, cfg)
    assert score > 0
    assert details["category_major"] in ["attractive", "performance", "must_be", "indifferent"]
    assert "KANO" in labels

def test_kano_satisfaction():
    agent = KanoAgent()
    task = Task(
        id="5",
        title="Heuristic Kano",
        metadata={"kano_satisfaction": 0.7, "kano_dissatisfaction": 0.3},
        created_at=datetime.now()
    )
    cfg = AnalysisConfig()
    score, details, labels = agent.score(task, cfg)
    assert score > 0
    assert labels["KANO"] in ["performance", "attractive", "indifferent"]

def test_moscow_basic():
    agent = MoSCoWAgent()
    task = Task(
        id="6",
        title="MoSCoW must",
        metadata={"moscow": "must"},
        created_at=datetime.now()
    )
    cfg = AnalysisConfig()
    score, details, labels = agent.score(task, cfg)
    assert score >= cfg.moscow.base_weights["must"]
    assert labels["MOSCOW"] == "must"

def test_moscow_with_deadline_and_dependency():
    agent = MoSCoWAgent()
    task = Task(
        id="7",
        title="Urgent dep",
        metadata={
            "moscow": "should",
            "critical_dependency": 1,
            "deadline_days": 5
        },
        created_at=datetime.now()
    )
    cfg = AnalysisConfig()
    score, details, _ = agent.score(task, cfg)
    assert score > details["base_weight"]

if __name__ == "__main__":
    pytest.main([__file__])



