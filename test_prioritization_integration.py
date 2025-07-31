


"""
Test Prioritization Integration with Decision Agent
"""

from agents.prioritization.prioritization_agent import PrioritizationAgent
from agents.prioritization.models import TaskData

def test_prioritization():
    """Test the prioritization agent directly"""

    # Create prioritization agent
    prioritization_agent = PrioritizationAgent()

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

    # Test prioritization
    print("Prioritization Results:")
    for idx, task in enumerate(tasks, 1):
        result = prioritization_agent.prioritize(TaskData(**task))
        print(f"\nTask {idx} ({task['title']}):")
        print(f"  Score: {result['score']['score']}")
        print(f"  Criticality: {result['criticality']}")
        print(f"  Is Bottleneck: {result['is_bottleneck']}")
        print(f"  Explanation: {result['explanation']}")

if __name__ == "__main__":
    test_prioritization()


