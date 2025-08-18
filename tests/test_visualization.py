















import pytest
from level2.visualization.visualization_aggregator import VisualizationAggregator
from level2.visualization.interactive_dashboard import InteractiveDashboardAgent
from level2.visualization.heatmap_generator import HeatmapGeneratorAgent
from level2.visualization.dependency_graph import DependencyGraphAgent
from level2.visualization.timeline_roadmap import TimelineRoadmapAgent

def test_interactive_dashboard():
    agent = InteractiveDashboardAgent()
    tasks = [{"id": "T1", "title": "Task 1", "status": "open"}, {"id": "T2", "title": "Task 2", "status": "closed"}]
    fig = agent.run(tasks)
    assert fig is not None

def test_heatmap_generator():
    agent = HeatmapGeneratorAgent()
    tasks = [
        {"id": "T1", "title": "Task 1", "value": 10, "effort": 5},
        {"id": "T2", "title": "Task 2", "value": 20, "effort": 10}
    ]
    fig = agent.run(tasks)
    assert fig is not None

def test_dependency_graph():
    agent = DependencyGraphAgent()
    tasks = [
        {"id": "T1", "title": "Task 1", "dependencies": ["T2"]},
        {"id": "T2", "title": "Task 2", "dependencies": []}
    ]
    fig = agent.run(tasks)
    assert fig is not None

def test_timeline_roadmap():
    agent = TimelineRoadmapAgent()
    tasks = [
        {"id": "T1", "title": "Task 1", "start_date": "2023-01-01", "end_date": "2023-01-10"},
        {"id": "T2", "title": "Task 2", "start_date": "2023-01-05", "end_date": "2023-01-15"}
    ]
    fig = agent.run(tasks)
    assert fig is not None

@pytest.mark.asyncio
async def test_visualization_aggregator():
    aggregator = VisualizationAggregator()
    tasks = [
        {"id": "T1", "title": "Task 1", "status": "open", "value": 10, "effort": 5, "dependencies": ["T2"],
         "start_date": "2023-01-01", "end_date": "2023-01-10"},
        {"id": "T2", "title": "Task 2", "status": "closed", "value": 20, "effort": 10, "dependencies": [],
         "start_date": "2023-01-05", "end_date": "2023-01-15"}
    ]
    results = await aggregator.run(tasks)
    assert "dashboard" in results
    assert "heatmap" in results
    assert "dependency_graph" in results
    assert "timeline" in results
    assert results["dashboard"] is not None
    assert results["heatmap"] is not None
    assert results["dependency_graph"] is not None
    assert results["timeline"] is not None

















