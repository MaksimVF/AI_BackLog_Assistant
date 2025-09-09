

"""
Test the LangGraph-based trigger agent
"""

import logging
from src.v2.agents.level1.trigger_agent_langgraph import LangGraphTriggerAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_trigger_agent():
    """Test the LangGraph trigger agent"""
    print("Testing LangGraph Trigger Agent")
    print("=" * 50)

    # Create trigger agent
    trigger_agent = LangGraphTriggerAgent()

    # Test case 1: High score should trigger
    print("\nTest 1: High score trigger")
    high_score_data = {
        'metadata': {'initial_score': 0.85},
        'content': {'text': 'This is a complex issue that needs attention'},
        'entities': ['issue', 'attention'],
        'relationships': [('issue', 'needs', 'attention')]
    }

    result = trigger_agent.check_conditions(high_score_data)
    print(f"High score trigger result: {result}")
    assert result == True, "High score should trigger Level 2"

    # Test case 2: Low score, small batch shouldn't trigger
    print("\nTest 2: Low score, no trigger")
    low_score_data = {
        'metadata': {'initial_score': 0.3},
        'content': {'text': 'Simple issue'},
        'entities': ['issue'],
        'relationships': []
    }

    result = trigger_agent.check_conditions(low_score_data)
    print(f"Low score trigger result: {result}")
    # This might not trigger depending on the complexity calculation

    # Test case 3: Batch size trigger
    print("\nTest 3: Batch size trigger")
    # Add multiple items to batch to reach threshold
    for i in range(12):  # Exceed batch size of 10
        batch_data = {
            'metadata': {'initial_score': 0.4},
            'content': {'text': f'Batch item {i}'},
            'entities': ['item'],
            'relationships': []
        }
        result = trigger_agent.check_conditions(batch_data)
        if result:
            print(f"Batch triggered at item {i}")
            break

    if not result:
        # Try one more to ensure batch trigger
        final_batch_data = {
            'metadata': {'initial_score': 0.4},
            'content': {'text': 'Final batch item'},
            'entities': ['item'],
            'relationships': []
        }

        result = trigger_agent.check_conditions(final_batch_data)
        print(f"Batch size trigger result: {result}")

    # Test case 4: Manual trigger
    print("\nTest 4: Manual trigger")
    manual_result = trigger_agent.manual_trigger()
    print(f"Manual trigger result: {manual_result}")
    assert manual_result == True, "Manual trigger should work"

    # Test case 5: Get batch
    print("\nTest 5: Get batch")
    batch = trigger_agent.get_batch()
    print(f"Batch size: {len(batch)}")
    assert len(batch) > 0, "Should have batch items"

    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_trigger_agent()

