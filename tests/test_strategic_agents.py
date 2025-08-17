



import pytest
import json
from datetime import datetime
from level2.dto import Task, AnalysisConfig
from level2.strategy.purpose_alignment import PurposeAlignmentAgent
from level2.strategy.impact_mapping import ImpactMappingAgent
from level2.strategy.cost_of_delay import CostOfDelayAgent
from level2.strategy.roi import RoiAgent

@pytest.fixture
def cfg():
    return AnalysisConfig()

def test_purpose_alignment(cfg):
    agent = PurposeAlignmentAgent()
    task = Task(
        id="1",
        project_id="test",
        title="OKR-aligned task",
        created_at=datetime.now(),
        metadata={
            "goals": json.dumps(["increase revenue", "improve user retention"]),
            "project_goals": json.dumps({
                "increase revenue by 20%": 0.8,
                "improve user retention by 10%": 0.6,
                "expand to new markets": 0.4
            })
        }
    )

    score, details, labels = agent.score(task, cfg)
    assert 0.0 <= score <= 1.0
    assert "PURPOSE" in labels
    assert "matched_goals" in details
    assert len(details["matched_goals"]) > 0

def test_impact_mapping(cfg):
    agent = ImpactMappingAgent()
    task = Task(
        id="2",
        project_id="test",
        title="High impact task",
        created_at=datetime.now(),
        metadata={
            "impact_targets": json.dumps([
                {"actor": "marketing", "impact": 0.8},
                {"actor": "sales", "impact": 0.7}
            ])
        }
    )

    score, details, labels = agent.score(task, cfg)
    assert 0.0 <= score <= 1.0
    assert "IMPACT_BIN" in labels
    assert "direct" in details
    assert len(details["direct"]["actors"]) == 2

def test_cost_of_delay(cfg):
    agent = CostOfDelayAgent()
    task = Task(
        id="3",
        project_id="test",
        title="Urgent task",
        created_at=datetime.now(),
        metadata={
            "value_per_day": "1000",
            "deadline_days": "7"
        }
    )

    score, details, labels = agent.score(task, cfg)
    assert 0.0 <= score <= 1.0
    assert "CoD_BIN" in labels
    assert "value_per_day" in details
    assert "urgency" in details

def test_roi(cfg):
    agent = RoiAgent()
    task = Task(
        id="4",
        project_id="test",
        title="High ROI task",
        created_at=datetime.now(),
        metadata={
            "expected_gain": "10000",
            "cost": "1000"
        }
    )

    score, details, labels = agent.score(task, cfg)
    assert 0.0 <= score <= 1.0
    assert "ROI_BIN" in labels
    assert "expected_gain" in details
    assert "cost" in details

def test_strategic_agents_with_missing_data(cfg):
    """Test that agents handle missing metadata gracefully"""
    task = Task(
        id="5",
        project_id="test",
        title="Task with missing data",
        created_at=datetime.now(),
        metadata={}
    )

    # Test all agents
    agents = [
        PurposeAlignmentAgent(),
        ImpactMappingAgent(),
        CostOfDelayAgent(),
        RoiAgent()
    ]

    for agent in agents:
        score, details, labels = agent.score(task, cfg)
        assert 0.0 <= score <= 1.0
        assert isinstance(details, dict)
        assert isinstance(labels, dict)


