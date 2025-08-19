



import pytest
from datetime import datetime
from level2.dto import Task, AnalysisConfig
from level2.scoring.orchestrator import PriorityOrchestrator
from level2.pipeline.orchestrator import Level2Orchestrator
from level2.scoring.stack_ranking import StackRankingAgent
from level2.scoring.value_vs_effort import ValueVsEffortAgent
from level2.scoring.opportunity_scoring import OpportunityScoringAgent
from level2.repository.mock_repo import MockRepository

@pytest.fixture
def cfg():
    return AnalysisConfig(
        methods=["STACK_RANKING", "VALUE_EFFORT", "OPPORTUNITY"],
        weights={"STACK_RANKING": 1.0, "VALUE_EFFORT": 1.0, "OPPORTUNITY": 0.8}
    )

@pytest.fixture
def orchestrator():
    agents = [StackRankingAgent(), ValueVsEffortAgent(), OpportunityScoringAgent()]
    return PriorityOrchestrator(agents)

def test_orchestrator_basic(cfg, orchestrator):
    task = Task(
        id="test1",
        project_id="test",
        title="Test task",
        created_at=datetime.now(),
        metadata={
            "votes": "80,70,90",
            "value": "8",
            "effort": "2",
            "importance": "9",
            "satisfaction": "3"
        }
    )

    result = orchestrator.analyze(task, cfg)

    # Check structure
    assert "by_method" in result
    assert "aggregate" in result
    assert "snapshots" in result

    # Check methods
    assert "STACK_RANKING" in result["by_method"]
    assert "VALUE_EFFORT" in result["by_method"]
    assert "OPPORTUNITY" in result["by_method"]

    # Check aggregate
    aggregate = result["aggregate"]
    assert "weighted_score" in aggregate
    assert "used_methods" in aggregate
    assert "normalization" in aggregate
    assert "per_method_norm" in aggregate

    # Check that weighted score is reasonable
    assert 0.0 <= aggregate["weighted_score"] <= 1.0

def test_orchestrator_ranking(cfg, orchestrator):
    tasks = [
        Task(
            id="high",
            project_id="test",
            title="High priority",
            created_at=datetime.now(),
            metadata={"votes": "90,95,100", "value": "10", "effort": "1", "importance": "10", "satisfaction": "1"}
        ),
        Task(
            id="low",
            project_id="test",
            title="Low priority",
            created_at=datetime.now(),
            metadata={"votes": "30,40,50", "value": "3", "effort": "5", "importance": "3", "satisfaction": "2"}
        )
    ]

    ranked = orchestrator.rank_tasks(tasks, cfg)

    # First task should be "high"
    assert ranked[0][0].id == "high"

    # Scores should be in descending order
    scores = [r[1]["aggregate"]["weighted_score"] for r in ranked]
    assert scores[0] >= scores[1]

def test_orchestrator_error_handling(cfg, orchestrator):
    # Create a task with missing metadata - agents should handle this gracefully
    task = Task(
        id="error_test",
        project_id="test",
        title="Error test",
        created_at=datetime.now(),
        metadata={}  # No data for agents
    )

    result = orchestrator.analyze(task, cfg)

    # Should still return a result even with missing data
    assert "by_method" in result
    assert "aggregate" in result

    # Check that all methods still return scores (no errors due to improved handling)
    assert all("score" in data for data in result["by_method"].values())

    # Check that aggregate score is reasonable
    assert 0.0 <= result["aggregate"]["weighted_score"] <= 1.0

def test_orchestrator_weights(cfg, orchestrator):
    task = Task(
        id="weight_test",
        project_id="test",
        title="Weight test",
        created_at=datetime.now(),
        metadata={
            "votes": "80,80,80",  # All agents should give similar scores
            "value": "5",
            "effort": "5",
            "importance": "5",
            "satisfaction": "5"
        }
    )

    # Test with custom weights
    custom_cfg = AnalysisConfig(
        methods=["STACK_RANKING", "VALUE_EFFORT", "OPPORTUNITY"],
        weights={"STACK_RANKING": 2.0, "VALUE_EFFORT": 0.5, "OPPORTUNITY": 1.0}
    )

    result = orchestrator.analyze(task, custom_cfg)

    # Check that weights are applied
    weights = result["aggregate"]["weights"]
    assert weights["STACK_RANKING"] == 2.0
    assert weights["VALUE_EFFORT"] == 0.5
    assert weights["OPPORTUNITY"] == 1.0

def test_level2_orchestrator_integration():
    """Test the Level2Orchestrator with all registered agents"""
    repo = MockRepository()

    # Create test tasks
    tasks = [
        Task(
            id="task1",
            project_id="test_project",
            title="High value, low effort task",
            metadata={
                "value": "9",
                "effort": "2",
                "importance": "8",
                "satisfaction": "3",
                "priority": "85",
                "moscow": "must"
            },
            created_at=datetime.now()
        ),
        Task(
            id="task2",
            project_id="test_project",
            title="Medium priority task",
            metadata={
                "value": "5",
                "effort": "5",
                "importance": "6",
                "satisfaction": "4",
                "priority": "50",
                "moscow": "should"
            },
            created_at=datetime.now()
        )
    ]

    repo.tasks = tasks

    # Create orchestrator
    orchestrator = Level2Orchestrator(repo)

    # Create analysis config with all available methods
    config = AnalysisConfig(
        methods=["RICE", "MOSCOW", "WSJF", "KANO", "VALUE_EFFORT", "OPPORTUNITY", "STACK_RANKING"],
        weights={
            "RICE": 1.0,
            "MOSCOW": 0.8,
            "WSJF": 1.0,
            "KANO": 1.0,
            "VALUE_EFFORT": 1.0,
            "OPPORTUNITY": 1.0,
            "STACK_RANKING": 0.9
        }
    )

    # Run analysis
    result = orchestrator.analyze_project("test_project", config)

    # Verify results
    assert result.project_id == "test_project"
    assert len(result.tasks) == 2

    # Check that all methods are represented
    for task_result in result.tasks:
        method_names = [ms.method for ms in task_result.method_scores]
        expected_methods = ["RICE", "MOSCOW", "WSJF", "KANO", "VALUE_EFFORT", "OPPORTUNITY", "STACK_RANKING"]

        # All requested methods should be present
        for method in expected_methods:
            assert method in method_names

        # Check that combined score is calculated
        assert task_result.combined_score is not None

        # Check that labels are aggregated
        assert len(task_result.labels) > 0


