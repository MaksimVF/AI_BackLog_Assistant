



"""
Integration test for Hybrid Content Classifier with LangGraph Trigger Agent
"""

import logging
from src.v2.agents.level1.content_classifier_hybrid import HybridContentClassifierAgent
from src.v2.agents.level1.trigger_agent_langgraph import LangGraphTriggerAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_integration():
    """Test the integration of hybrid classifier with LangGraph trigger agent"""
    print("Testing Integration: Hybrid Classifier + LangGraph Trigger")
    print("=" * 60)

    # Create agents
    classifier = HybridContentClassifierAgent()
    trigger_agent = LangGraphTriggerAgent()

    # Test case 1: High priority feature request
    print("\nTest 1: High priority feature request")
    feature_text = "This is an urgent feature request for our enterprise customers. We need to add multi-factor authentication to comply with security regulations. This is critical for our business."
    classified_data = classifier.classify({'content': feature_text})
    print(f"Classification: {classified_data['metadata']}")

    should_trigger = trigger_agent.check_conditions(classified_data)
    print(f"Should trigger Level 2: {should_trigger}")
    assert should_trigger == True, "High priority feature should trigger Level 2"

    # Test case 2: Simple question (should not trigger)
    print("\nTest 2: Simple question")
    question_text = "How do I change my password?"
    classified_data = classifier.classify({'content': question_text})
    print(f"Classification: {classified_data['metadata']}")

    should_trigger = trigger_agent.check_conditions(classified_data)
    print(f"Should trigger Level 2: {should_trigger}")
    assert should_trigger == False, "Simple question should not trigger Level 2"

    # Test case 3: Marketing campaign idea
    print("\nTest 3: Marketing campaign idea")
    marketing_text = "I have an idea for a viral marketing campaign that could reach millions of users. We should partner with influencers and create engaging content around our new product launch."
    classified_data = classifier.classify({'content': marketing_text})
    print(f"Classification: {classified_data['metadata']}")

    should_trigger = trigger_agent.check_conditions(classified_data)
    print(f"Should trigger Level 2: {should_trigger}")
    assert should_trigger == True, "Marketing campaign idea should trigger Level 2"

    # Test case 4: Multiple items in batch
    print("\nTest 4: Batch processing")
    # Add several items to batch
    for i in range(8):
        item_text = f"Simple user feedback item {i+1}"
        classified_data = classifier.classify({'content': item_text})
        trigger_agent.check_conditions(classified_data)

    # Add one more to reach batch threshold
    final_text = "One more simple feedback item"
    classified_data = classifier.classify({'content': final_text})
    should_trigger = trigger_agent.check_conditions(classified_data)
    print(f"Should trigger Level 2 due to batch size: {should_trigger}")
    assert should_trigger == True, "Batch size should trigger Level 2"

    print("\n✅ All integration tests passed!")

if __name__ == "__main__":
    test_integration()



