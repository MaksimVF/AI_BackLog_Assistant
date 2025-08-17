

#!/usr/bin/env python3

"""
Test script for Level 2 implementation
"""

import os
import weaviate
from datetime import datetime
from level2.dto import Task, AnalysisConfig
from level2.repository.weaviate_repo import WeaviateRepository
from level2.pipeline.orchestrator import Level2Orchestrator

def test_level2_analysis():
    """Test the Level 2 analysis pipeline"""

    # Create a simple mock repository instead of mocking Weaviate client
    class MockRepository:
        def fetch_tasks(self, project_id: str):
            return [
                Task(
                    id="task1",
                    project_id="test_project",
                    title="Test Task 1",
                    description="Test description",
                    tags=["test", "example"],
                    effort=5.0,
                    reach=10.0,
                    impact=8.0,
                    confidence=0.9,
                    dependencies=[],
                    metadata={"moscow": "must"},
                    created_at=datetime.now()
                )
            ]

        def save_analysis(self, result):
            print(f"Saved analysis for project: {result.project_id}")

        def update_task_labels(self, task_id: str, labels: dict):
            print(f"Updated labels for task {task_id}: {labels}")

    # Create mock repository
    repo = MockRepository()

    # Create orchestrator
    orchestrator = Level2Orchestrator(repo)

    # Create analysis config
    config = AnalysisConfig(
        methods=["RICE", "MOSCOW"],
        weights={"RICE": 1.0, "MOSCOW": 0.8}
    )

    # Run analysis
    result = orchestrator.analyze_project("test_project", config)

    # Print results
    print("Analysis Results:")
    print(f"Project ID: {result.project_id}")
    print(f"Number of tasks analyzed: {len(result.tasks)}")
    print(f"Config used: {result.config_used}")

    for task_analysis in result.tasks:
        print(f"\nTask ID: {task_analysis.task_id}")
        print(f"Combined Score: {task_analysis.combined_score}")
        print("Method Scores:")
        for method_score in task_analysis.method_scores:
            print(f"  {method_score.method}: {method_score.score} (details: {method_score.details})")
        print(f"Labels: {task_analysis.labels}")

    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_level2_analysis()

