





"""
Test Output Agent
"""

from agents.output.output_agent import OutputAgent, OutputMode, OutputFormat

def test_output_agent():
    """Test the output agent with sample data"""

    # Sample input data
    task_id = "task_123"
    decision_result = {
        "status": "recommended",
        "explanation": "High priority task with critical impact",
        "confidence": "high"
    }
    priority_data = {
        "priority_score": 85,
        "rice_score": 72
    }
    effort_data = {
        "effort_estimate": "3 days",
        "effort_hours": 24
    }
    deadline = "2025-08-15"
    visuals = {
        "charts": ["priority_chart.png", "effort_chart.png"],
        "tables": ["task_summary.csv"]
    }
    schedule = {
        "due_date": "2025-08-15",
        "checkpoints": ["2025-08-10", "2025-08-13"],
        "reminders": ["2025-08-08", "2025-08-14"]
    }

    # Test different user profiles
    user_profiles = [
        {"subscription": "free", "is_authenticated": False},
        {"subscription": "pro", "is_authenticated": True},
        {"subscription": "enterprise", "is_authenticated": True}
    ]

    # Test different output modes and formats
    test_cases = [
        {"mode": OutputMode.UI, "format": OutputFormat.JSON, "name": "UI JSON"},
        {"mode": OutputMode.API, "format": OutputFormat.JSON, "name": "API JSON"},
        {"mode": OutputMode.FILE, "format": OutputFormat.JSON, "name": "File JSON"},
        {"mode": OutputMode.UI, "format": OutputFormat.MARKDOWN, "name": "UI Markdown"},
        {"mode": OutputMode.UI, "format": OutputFormat.HTML, "name": "UI HTML"},
        {"mode": OutputMode.UI, "format": OutputFormat.TEXT, "name": "UI Text"}
    ]

    print("Testing Output Agent...")
    for user_profile in user_profiles:
        print(f"\n{'='*60}")
        print(f"User Profile: {user_profile['subscription']} subscription, Authenticated: {user_profile['is_authenticated']}")

        for test_case in test_cases:
            print(f"\n--- {test_case['name']} ---")

            # Create output agent
            output_agent = OutputAgent(
                mode=test_case["mode"],
                user_profile=user_profile,
                compact_mode=True,
                enable_logging=False,
                output_format=test_case["format"]
            )

            # Process output
            result = output_agent.process(
                task_id=task_id,
                decision_result=decision_result,
                priority_data=priority_data,
                effort_data=effort_data,
                deadline=deadline,
                visuals=visuals,
                schedule=schedule
            )

            # Display result
            if isinstance(result, dict):
                print(f"Result type: {type(result).__name__}")
                print(f"Status: {result.get('status', 'N/A')}")
                print(f"Summary: {result.get('summary', 'N/A')}")
                if "note" in result:
                    print(f"Note: {result['note']}")
            elif isinstance(result, str):
                print(f"Result type: {type(result).__name__}")
                print(f"Output (first 100 chars): {result[:100]}...")

if __name__ == "__main__":
    test_output_agent()





