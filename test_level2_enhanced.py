




from level2.dto import Task, AnalysisConfig, RiceConfig, WsjfConfig, KanoConfig, MoscowConfig
from level2.pipeline.orchestrator import Level2Orchestrator
from level2.repository.mock_repo import MockRepository
from datetime import datetime

def test_level2_enhanced():
    print("Testing Level 2 with enhanced agents...")

    # Create mock repository
    repo = MockRepository()

    # Create test tasks
    tasks = [
        Task(
            id="task1",
            project_id="test_project",
            title="High impact feature",
            reach=8000,
            impact=3.0,
            confidence=0.9,
            effort=5,
            metadata={
                "risk_prob": "0.2",
                "risk_impact": "0.3",
                "bv": "10",
                "tc": "7",
                "rr_oe": "4",
                "kano_satisfaction": "0.8",
                "kano_dissatisfaction": "0.2",
                "moscow": "must",
                "critical_dependency": "1",
                "deadline_days": "3"
            },
            created_at=datetime.now()
        ),
        Task(
            id="task2",
            project_id="test_project",
            title="Medium priority task",
            reach=3000,
            impact=2.0,
            confidence=0.7,
            effort=3,
            metadata={
                "risk_prob": "0.1",
                "risk_impact": "0.2",
                "bv": "5",
                "tc": "3",
                "rr_oe": "2",
                "kano_satisfaction": "0.6",
                "kano_dissatisfaction": "0.3",
                "moscow": "should",
                "deadline_days": "10"
            },
            created_at=datetime.now()
        )
    ]

    repo.tasks = tasks

    # Create orchestrator
    orchestrator = Level2Orchestrator(repo)

    # Create analysis config with enhanced settings
    config = AnalysisConfig(
        methods=["RICE", "MOSCOW", "WSJF", "KANO"],
        weights={"RICE": 1.0, "MOSCOW": 0.8, "WSJF": 1.0, "KANO": 1.0},
        rice=RiceConfig(reach_min=0, reach_max=10000, risk_penalty=0.3),
        wsjf=WsjfConfig(min_score=1, max_score=10),
        kano=KanoConfig(weight_attractive=1.2),
        moscow=MoscowConfig(deadline_boost=0.15)
    )

    # Run analysis
    result = orchestrator.analyze_project("test_project", config)

    # Print results
    print("Analysis Results:")
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

    print("\n🎉 Level 2 enhanced test completed successfully!")

if __name__ == "__main__":
    test_level2_enhanced()






