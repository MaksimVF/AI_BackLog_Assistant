

import pytest
from agents.third_level.decision_recommender import DecisionRecommenderAgent

@pytest.mark.asyncio
async def test_accelerate_decision():
    agent = DecisionRecommenderAgent(rice_threshold=5, wsjf_threshold=5)
    # подсовываем сигналы напрямую
    meta = {"scores": {"RICE": 9, "WSJF": 8}, "risk": {"level": 0.2}}
    decision = agent._decide(meta)
    assert decision["recommendation"] == "accelerate"

@pytest.mark.asyncio
async def test_delay_decision():
    agent = DecisionRecommenderAgent(risk_delay_threshold=0.6)
    meta = {"scores": {"RICE": 4, "WSJF": 4}, "risk": {"level": 0.8}}
    decision = agent._decide(meta)
    assert decision["recommendation"] == "delay"

@pytest.mark.asyncio
async def test_drop_decision():
    agent = DecisionRecommenderAgent(low_value_threshold=2.0)
    meta = {"scores": {"RICE": 3, "WSJF": 3}, "value": 1.0}
    decision = agent._decide(meta)
    assert decision["recommendation"] == "drop"

@pytest.mark.asyncio
async def test_merge_decision():
    agent = DecisionRecommenderAgent()
    meta = {"value": 3.0, "effort": 20}
    decision = agent._decide(meta)
    assert decision["recommendation"] == "merge"

