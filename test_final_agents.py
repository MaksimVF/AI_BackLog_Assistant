




from level2.dto import Task, AnalysisConfig
from level2.scoring.rice import RiceAgent
from level2.scoring.wsjf import WSJFAgent
from level2.scoring.kano import KanoAgent
from level2.scoring.moscow import MoSCoWAgent
from datetime import datetime

def test_all_agents():
    print("Testing all enhanced agents...")

    # Create test task
    task = Task(
        id="test1",
        project_id="test_project",
        title="Test Task",
        reach=5000,
        impact=2.0,
        confidence=0.8,
        effort=5,
        metadata={
            "risk_prob": "0.3",
            "risk_impact": "0.4",
            "bv": "8",
            "tc": "5",
            "rr_oe": "3",
            "kano_satisfaction": "0.7",
            "kano_dissatisfaction": "0.3",
            "moscow": "must",
            "critical_dependency": "1",
            "deadline_days": "7"
        },
        created_at=datetime.now()
    )

    cfg = AnalysisConfig()

    # Test RICE
    print("\n--- Testing RICE ---")
    rice_agent = RiceAgent()
    rice_score, rice_details, rice_labels = rice_agent.score(task, cfg)
    print(f"RICE score: {rice_score}")
    print(f"Details: {rice_details}")
    print(f"Labels: {rice_labels}")

    # Test WSJF
    print("\n--- Testing WSJF ---")
    wsjf_agent = WSJFAgent()
    wsjf_score, wsjf_details, wsjf_labels = wsjf_agent.score(task, cfg)
    print(f"WSJF score: {wsjf_score}")
    print(f"Details: {wsjf_details}")
    print(f"Labels: {wsjf_labels}")

    # Test Kano
    print("\n--- Testing Kano ---")
    kano_agent = KanoAgent()
    kano_score, kano_details, kano_labels = kano_agent.score(task, cfg)
    print(f"Kano score: {kano_score}")
    print(f"Details: {kano_details}")
    print(f"Labels: {kano_labels}")

    # Test MoSCoW
    print("\n--- Testing MoSCoW ---")
    moscow_agent = MoSCoWAgent()
    moscow_score, moscow_details, moscow_labels = moscow_agent.score(task, cfg)
    print(f"MoSCoW score: {moscow_score}")
    print(f"Details: {moscow_details}")
    print(f"Labels: {moscow_labels}")

    print("\n🎉 All agents tested successfully!")

if __name__ == "__main__":
    test_all_agents()





