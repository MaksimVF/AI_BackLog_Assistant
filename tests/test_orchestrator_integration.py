


import pytest
from datetime import datetime
from level2.dto import Task, AnalysisConfig
from level2.pipeline.orchestrator import Level2Orchestrator
from level2.repository.mock_repo import MockRepository

def test_orchestrator_all_agents():
    """Test that the Level2Orchestrator can handle all scoring agents"""
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
            assert method in method_names, f"Method {method} not found in task scores"

        # Check that combined score is calculated
        assert task_result.combined_score is not None

        # Check that labels are aggregated
        assert len(task_result.labels) > 0

def test_orchestrator_subset_agents():
    """Test that the Level2Orchestrator can handle a subset of scoring agents"""
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
        )
    ]

    repo.tasks = tasks

    # Create orchestrator
    orchestrator = Level2Orchestrator(repo)

    # Create analysis config with a subset of methods
    config = AnalysisConfig(
        methods=["RICE", "WSJF", "VALUE_EFFORT"],
        weights={
            "RICE": 1.0,
            "WSJF": 1.0,
            "VALUE_EFFORT": 1.0
        }
    )

    # Run analysis
    result = orchestrator.analyze_project("test_project", config)

    # Verify results
    assert result.project_id == "test_project"
    assert len(result.tasks) == 1

    # Check that only requested methods are present
    for task_result in result.tasks:
        method_names = [ms.method for ms in task_result.method_scores]
        expected_methods = ["RICE", "WSJF", "VALUE_EFFORT"]

        # All requested methods should be present
        for method in expected_methods:
            assert method in method_names

        # No unexpected methods should be present
        for method in method_names:
            assert method in expected_methods

        # Check that combined score is calculated
        assert task_result.combined_score is not None

def test_orchestrator_default_config():
    """Test that the Level2Orchestrator works with default config"""
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
        )
    ]

    repo.tasks = tasks

    # Create orchestrator
    orchestrator = Level2Orchestrator(repo)

    # Run analysis with default config
    result = orchestrator.analyze_project("test_project", AnalysisConfig())

    # Verify results
    assert result.project_id == "test_project"
    assert len(result.tasks) == 1

    # Check that some methods are present (default config should include some)
    for task_result in result.tasks:
        method_names = [ms.method for ms in task_result.method_scores]
        assert len(method_names) > 0

        # Check that combined score is calculated
        assert task_result.combined_score is not None


