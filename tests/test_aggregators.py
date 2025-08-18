












import pytest
from level2.teamwork.teamwork_aggregator import TeamworkAggregator
from level2.analytics.analytics_aggregator import AnalyticsAggregator

@pytest.mark.asyncio
async def test_teamwork_aggregator():
    aggregator = TeamworkAggregator()
    tasks = [{"id": "T1", "title": "Test Task"}]
    votes = {"project_id": "P1", "task_id": "T1", "votes": [{"voter_id": "U1", "value": "yes"}]}
    results = await aggregator.run(tasks, votes)
    assert "voting" in results
    assert "conflicts" in results
    assert "stakeholder_alignment" in results

@pytest.mark.asyncio
async def test_analytics_aggregator():
    aggregator = AnalyticsAggregator()
    tasks = [{"id": "T1", "title": "Test Task", "metadata": {"history_efforts": [1, 2, 3]}}]
    history = [{"id": "T1", "title": "Test Task", "metadata": {"est_effort": 5, "actual_effort": 10, "delay_days": 5}}]
    results = await aggregator.run(tasks, history)
    assert "trends" in results
    assert "risks" in results
    assert "dependencies" in results
    assert "effort_forecast" in results
    assert "forensic" in results

@pytest.mark.asyncio
async def test_analytics_aggregator_no_history():
    aggregator = AnalyticsAggregator()
    tasks = [{"id": "T1", "title": "Test Task", "metadata": {"history_efforts": [1, 2, 3]}}]
    results = await aggregator.run(tasks)
    assert "trends" in results
    assert "risks" in results
    assert "dependencies" in results
    assert "effort_forecast" in results
    assert "forensic" not in results













