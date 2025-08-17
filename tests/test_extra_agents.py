

import pytest
from level2.dto import Task, AnalysisConfig
from level2.scoring.stack_ranking import StackRankingAgent
from level2.scoring.value_vs_effort import ValueVsEffortAgent
from level2.scoring.opportunity_scoring import OpportunityScoringAgent
from datetime import datetime

@pytest.fixture
def cfg():
    return AnalysisConfig()

def test_stack_ranking_votes(cfg):
    agent = StackRankingAgent()
    task = Task(
        id="1",
        project_id="test_project",
        title="Stack rank",
        created_at=datetime.now(),
        metadata={"votes": "80,70,90"}  # Store as string
    )
    score, details, labels = agent.score(task, cfg)
    assert details["avg_vote"] == 80
    assert 7 <= score <= 10
    assert labels["STACK_BIN"] == "HIGH"

def test_value_vs_effort(cfg):
    agent = ValueVsEffortAgent()
    task = Task(
        id="2",
        project_id="test_project",
        title="Value vs Effort",
        effort=2,
        created_at=datetime.now(),
        metadata={"value": "8"}  # Store as string
    )
    score, details, labels = agent.score(task, cfg)
    assert score > 0
    assert labels["VALUE_EFFORT_BIN"] in ["HIGH", "MEDIUM", "LOW"]

def test_opportunity_scoring(cfg):
    agent = OpportunityScoringAgent()
    task = Task(
        id="3",
        project_id="test_project",
        title="Opportunity case",
        created_at=datetime.now(),
        metadata={"importance": "9", "satisfaction": "3"}  # Store as strings
    )
    score, details, labels = agent.score(task, cfg)
    assert score == 6
    assert labels["OPPORTUNITY_BIN"] == "MEDIUM"

