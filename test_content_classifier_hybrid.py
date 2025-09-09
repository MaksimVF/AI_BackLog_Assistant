



"""
Test the Hybrid Content Classifier Agent
"""

import logging
from src.v2.agents.level1.content_classifier_hybrid import HybridContentClassifierAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_hybrid_classifier():
    """Test the hybrid content classifier"""
    print("Testing Hybrid Content Classifier")
    print("=" * 50)

    classifier = HybridContentClassifierAgent()

    # Test case 1: Feature request
    print("\nTest 1: Feature request")
    feature_text = "I would like to see a new feature that allows users to export data as CSV. This would be really helpful for our workflow."
    result = classifier.classify({'content': feature_text})
    print(f"Result: {result['metadata']}")
    assert result['metadata']['content_type'] == 'feature_request'
    assert result['metadata']['primary_emotion'] == 'positive'
    assert result['metadata']['initial_score'] > 0.7

    # Test case 2: Bug report
    print("\nTest 2: Bug report")
    bug_text = "The application crashes when I try to save a large file. This is a critical issue that needs to be fixed ASAP."
    result = classifier.classify({'content': bug_text})
    print(f"Result: {result['metadata']}")
    assert result['metadata']['content_type'] == 'bug_report'
    assert 'urgent' in result['metadata']['emotions']
    assert result['metadata']['initial_score'] > 0.6  # Bug reports have lower score due to negative emotion

    # Test case 3: Marketing idea
    print("\nTest 3: Marketing idea")
    marketing_text = "We should run a social media campaign targeting young professionals. This could boost our brand awareness."
    result = classifier.classify({'content': marketing_text})
    print(f"Result: {result['metadata']}")
    assert result['metadata']['content_type'] == 'marketing_idea'
    assert result['metadata']['domain'] == 'digital_marketing'

    # Test case 4: Technical question
    print("\nTest 4: Technical question")
    tech_text = "How do I configure the API to work with our existing system? I'm having trouble with authentication."
    result = classifier.classify({'content': tech_text})
    print(f"Result: {result['metadata']}")
    assert result['metadata']['content_type'] == 'technical_question'
    assert result['metadata']['domain'] == 'software_development'

    # Test case 5: Content request
    print("\nTest 5: Content request")
    content_text = "Can you create a blog post about the benefits of our new product? We need it for next week."
    result = classifier.classify({'content': content_text})
    print(f"Result: {result['metadata']}")
    assert result['metadata']['content_type'] == 'content_request'
    assert result['metadata']['domain'] == 'content_creation'

    # Test case 6: Billing question
    print("\nTest 6: Billing question")
    billing_text = "I have a question about my invoice. The amount seems higher than expected."
    result = classifier.classify({'content': billing_text})
    print(f"Result: {result['metadata']}")
    assert result['metadata']['content_type'] == 'billing_question'
    assert result['metadata']['domain'] == 'finance'

    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_hybrid_classifier()



