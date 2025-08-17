



import pytest
from level2.teamwork.agents.voting_consensus import VotingConsensusAgent
from level2.teamwork.agents.conflict_resolution import ConflictResolutionAgent
from level2.teamwork.agents.stakeholder_alignment import StakeholderAlignmentAgent
from level2.teamwork.dto import Vote, VoteRequest, VotingConfig, ConflictConfig
from level2.dto import Task

def test_voting_simple_yes():
    agent = VotingConsensusAgent()
    votes = [Vote(voter_id="u1", value="yes"), Vote(voter_id="u2", value="yes"), Vote(voter_id="u3", value="no")]
    vr = VoteRequest(project_id="p", task_id="t", votes=votes, vote_scheme="binary")
    res, internals = agent.score(vr, VotingConfig(quorum_ratio=0.3, consensus_threshold=0.6))
    assert res.quorum is True
    assert res.decision in ("approve","reject","no_consensus")

def test_voting_weighted():
    agent = VotingConsensusAgent()
    votes = [Vote(voter_id="a", value="yes", weight=3), Vote(voter_id="b", value="no", weight=1)]
    vr = VoteRequest(project_id="p", task_id="t", votes=votes, vote_scheme="binary")
    res, _ = agent.score(vr, VotingConfig(quorum_ratio=0.5, consensus_threshold=0.66))
    assert res.total_weight == 4
    assert res.yes_weight == 3
    assert res.decision == "approve"

def test_conflict_binary_even_split():
    agent = ConflictResolutionAgent()
    votes = [Vote(voter_id="u1", value="yes"), Vote(voter_id="u2", value="no"), Vote(voter_id="u3", value="yes"), Vote(voter_id="u4", value="no")]
    vr = VoteRequest(project_id="p", task_id="t", votes=votes, vote_scheme="binary")
    severity, details = agent.score(vr, ConflictConfig(severity_threshold=0.4))
    assert 0.0 <= severity <= 1.0
    assert "severity_raw" in details or "level" in details

def test_conflict_numerical():
    agent = ConflictResolutionAgent()
    votes = [Vote(voter_id="u1", value=1.0), Vote(voter_id="u2", value=0.1), Vote(voter_id="u3", value=0.9)]
    vr = VoteRequest(project_id="p", task_id="t", votes=votes, vote_scheme="score")
    severity, details = agent.score(vr, ConflictConfig(severity_threshold=0.2))
    assert 0.0 <= severity <= 1.0
    assert "normalized_std" in details

def test_stakeholder_alignment_basic():
    agent = StakeholderAlignmentAgent()
    # task has two stakeholders priorities
    task = Task(id="t1", title="x", metadata={"priority_vector": {"s1": 0.8, "s2": 0.2}})
    project_stakeholders = {"s1": {"weight": 2.0}, "s2": {"weight": 1.0}}
    score, details, labels = agent.score(task, project_stakeholders=project_stakeholders, cfg=None)
    assert 0.0 <= score <= 1.0





