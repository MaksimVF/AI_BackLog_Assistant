

#!/usr/bin/env python3

"""
Test script to verify the integration of newly registered agents
"""

from datetime import datetime
from level2.dto import Task, AnalysisConfig
from level2.pipeline.orchestrator import Level2Orchestrator
from level2.repository.mock_repo import MockRepository

def test_new_agents_integration():
    """Test the integration of newly registered agents"""

    # Create mock repository
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

    # Print results
    print("Analysis Results with New Agents:")
    print(f"Project ID: {result.project_id}")
    print(f"Number of tasks analyzed: {len(result.tasks)}")
    print(f"Config used: {result.config_used}")

    for task_result in result.tasks:
        print(f"\nTask: {task_result.task_id}")
        print(f"Combined score: {task_result.combined_score:.3f}")
        print("Method scores:")
        for method_score in task_result.method_scores:
            print(f"  {method_score.method}: {method_score.score:.3f} (details: {method_score.details})")
        print(f"Labels: {task_result.labels}")

    print("\n🎉 All new agents integration test completed successfully!")

if __name__ == "__main__":
    test_new_agents_integration()

