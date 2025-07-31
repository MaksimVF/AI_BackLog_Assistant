

"""
Test Decision Agent Integration
"""

from agents.prioritization.decision_agent_integration import DecisionAgent
from agents.prioritization.models import TaskData

def test_decision_agent():
    """Test the decision agent with sample tasks"""

    # Create decision agent
    agent = DecisionAgent()

    # Sample tasks
    tasks = [
        {
            "task_id": "task_1",
            "title": "Critical security fix",
            "description": "Fix critical vulnerability in authentication system",
            "impact": 9,
            "urgency": 8,
            "is_blocking": True,
            "effort": 2
        },
        {
            "task_id": "task_2",
            "title": "UI improvement",
            "description": "Enhance button styles",
            "impact": 5,
            "urgency": 3,
            "effort": 1
        },
        {
            "task_id": "task_3",
            "title": "Documentation update",
            "description": "Update API documentation",
            "impact": 3,
            "urgency": 2,
            "effort": 2
        }
    ]

    # Test individual decisions
    print("Individual Task Decisions:")
    for idx, task in enumerate(tasks, 1):
        result = agent.make_decision(TaskData(**task))
        print(f"\nTask {idx} ({task['title']}):")
        print(f"  Decision: {result['decision']}")
        print(f"  Report: {result['report']}")
        print(f"  Priority Analysis: {result['priority_analysis']}")

    # Test batch decisions
    print("\n\nBatch Decision Results:")
    batch_results = agent.batch_decision([TaskData(**task) for task in tasks])

    for idx, result in enumerate(batch_results, 1):
        print(f"\nTask {idx} Decision: {result['decision']}")

if __name__ == "__main__":
    test_decision_agent()

