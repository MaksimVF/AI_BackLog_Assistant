



"""
Test Execution Planner Agent
"""

from datetime import datetime
from agents.execution_planner.execution_planner_agent import ExecutionPlannerAgent

def test_execution_planner():
    """Test the execution planner agent with sample tasks"""

    # Create execution planner agent
    planner = ExecutionPlannerAgent()

    # Sample tasks with decisions
    tasks = [
        {
            "task_id": "task_1",
            "title": "Critical security fix",
            "description": "Fix critical vulnerability in authentication system. Requires API integration.",
            "priority": "high",
            "criticality": "high",
            "estimated_effort_days": 2,
            "effort_hours": 12,
            "dependencies": ["task_102"],
            "stakeholders": ["security_team", "api_team"],
            "assigned_to": "security_lead",
            "category": "Security",
            "priority_score": 8.5,
            "strategic_alignment": True,
            "team_size": 3,
            "budget": 10000
        },
        {
            "task_id": "task_2",
            "title": "UI improvement",
            "description": "Enhance button styles and colors",
            "priority": "medium",
            "criticality": "low",
            "estimated_effort_days": 1,
            "effort_hours": 6,
            "dependencies": [],
            "stakeholders": ["design_team"],
            "assigned_to": "ui_designer",
            "category": "UI/UX",
            "priority_score": 5.0,
            "strategic_alignment": True,
            "team_size": 1,
            "budget": 2000
        },
        {
            "task_id": "task_3",
            "title": "Documentation update",
            "description": "Update API documentation for new endpoints",
            "priority": "low",
            "criticality": "low",
            "estimated_effort_days": 3,
            "effort_hours": 18,
            "dependencies": [],
            "stakeholders": ["doc_team"],
            "assigned_to": "tech_writer",
            "category": "Documentation",
            "priority_score": 3.0,
            "strategic_alignment": False,
            "team_size": 1,
            "budget": 1000
        }
    ]

    # Test individual execution plans
    print("Execution Planner Results:")
    for idx, task in enumerate(tasks, 1):
        # Simulate decision from DecisionAgent
        decision = "recommend" if task["priority_score"] >= 5 else "defer"

        result = planner.plan_execution(task, decision)
        print(f"\n{'='*60}")
        print(f"Task {idx} ({task['title']}):")
        print(f"  Original Decision: {decision}")
        print(f"  Final Decision: {result['final_decision']['decision']}")
        print(f"  Reason: {result['final_decision']['reason']}")
        print(f"  Estimated Duration: {result['timeline_estimation']['estimated_duration_days']} days")
        print(f"  Deadline: {result['deadline_calculation']['deadline_date']}")
        print(f"  Dependencies: {len(result['dependency_analysis']['dependency_details'])}")
        print(f"  Risks: {len(result['risk_assessment']['risk_assessment'])}")
        print(f"  Follow-ups: {len(result['followup_notifications']['reminder_schedule'])} reminders, {len(result['followup_notifications']['checkpoints'])} checkpoints")

    # Test batch execution planning
    print(f"\n{'='*60}")
    print("Batch Execution Planning Summary:")
    batch_tasks = [
        {"task": task, "decision": "recommend" if task["priority_score"] >= 5 else "defer"}
        for task in tasks
    ]
    batch_results = planner.plan_batch_execution(batch_tasks)

    for idx, result in enumerate(batch_results, 1):
        print(f"Task {idx}: {result['final_decision']['decision']} - {result['final_decision']['reason']}")

if __name__ == "__main__":
    test_execution_planner()



