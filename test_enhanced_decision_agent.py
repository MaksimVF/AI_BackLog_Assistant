


"""
Test Enhanced Decision Agent with Multiple Sub-Agents
"""

from agents.prioritization.enhanced_decision_agent import EnhancedDecisionAgent
from agents.prioritization.models import TaskData
from datetime import datetime, timedelta

def test_enhanced_decision_agent():
    """Test the enhanced decision agent with comprehensive task data"""

    # Create enhanced decision agent
    agent = EnhancedDecisionAgent()

    # Sample tasks with comprehensive data
    tasks = [
        {
            "task_id": "task_1",
            "title": "Critical security fix",
            "description": "Fix critical vulnerability in authentication system",
            "impact": 9,
            "urgency": 8,
            "is_blocking": True,
            "effort": 2,
            "deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "uncertainty_level": "low",
            "required_skills": ["python", "security"],
            "team_expertise": {"python": "high", "security": "medium"},
            "available_hours": 40,
            "estimated_time_hours": 16,
            "dependencies": ["task_102"],
            "user_feedback": [
                {"sentiment": "positive", "comment": "This is crucial for our security"}
            ],
            "type": "bug",
            "external_dependencies": ["security_audit"]
        },
        {
            "task_id": "task_2",
            "title": "UI improvement",
            "description": "Enhance button styles",
            "impact": 5,
            "urgency": 3,
            "effort": 1,
            "deadline": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "uncertainty_level": "medium",
            "required_skills": ["css", "javascript"],
            "team_expertise": {"css": "high", "javascript": "medium"},
            "available_hours": 20,
            "estimated_time_hours": 8,
            "user_feedback": [
                {"sentiment": "neutral", "comment": "Would be nice to have"}
            ],
            "type": "feature"
        },
        {
            "task_id": "task_3",
            "title": "Documentation update",
            "description": "Update API documentation",
            "impact": 3,
            "urgency": 2,
            "effort": 2,
            "deadline": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "uncertainty_level": "low",
            "required_skills": ["technical_writing"],
            "team_expertise": {"technical_writing": "medium"},
            "available_hours": 10,
            "estimated_time_hours": 5,
            "user_feedback": [
                {"sentiment": "negative", "comment": "Not very useful"}
            ],
            "type": "documentation"
        }
    ]

    # Test individual decisions
    print("Enhanced Decision Agent Results:")
    for idx, task in enumerate(tasks, 1):
        result = agent.make_decision(TaskData(**task))
        print(f"\n{'='*60}")
        print(f"Task {idx} ({task['title']}):")
        print(f"  Decision: {result['decision']}")
        print(f"  Report: {result['report']}")
        print(f"  Priority Analysis Score: {result['priority_analysis']['score']['score']}")
        print(f"  Risk: {result['sub_agent_analyses']['risk']['risk_label']}")
        print(f"  Resources: {result['sub_agent_analyses']['resource']['resource_label']}")
        print(f"  Urgency: {result['sub_agent_analyses']['deadline']['urgency_label']}")
        print(f"  Dependencies: {result['sub_agent_analyses']['dependency']['dependency_severity']}")
        print(f"  Feedback: {result['sub_agent_analyses']['feedback']['feedback_label']}")
        print(f"  Compliance: {result['sub_agent_analyses']['compliance']['compliance_level']}")

    # Test batch decisions
    print(f"\n{'='*60}")
    print("Batch Decision Summary:")
    batch_results = agent.batch_decision([TaskData(**task) for task in tasks])

    for idx, result in enumerate(batch_results, 1):
        print(f"Task {idx}: {result['decision']}")

if __name__ == "__main__":
    test_enhanced_decision_agent()


