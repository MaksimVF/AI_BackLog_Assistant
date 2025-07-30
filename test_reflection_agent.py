





#!/usr/bin/env python3

"""Test script for Reflection Agent"""

from agents.reflection_agent import ReflectionAgent, ReflectionInput

def test_reflection_agent():
    """Test the Reflection Agent with different inputs"""

    # Create reflection agent with mock memory
    class MockMemory:
        def find_similar_case(self, text):
            return None

        def store_case(self, case_id, content, context, domain_tags, metadata, user_id=None):
            return {}

        def query_similar_cases(self, text, limit=3):
            return []

    agent = ReflectionAgent(memory=MockMemory())

    # Test cases with expected intents and user IDs
    test_cases = [
        {
            "content": "Я чувствую себя очень подавленно на работе, не знаю как справиться со стрессом.",
            "expected_context": "личный",
            "expected_intent": "вопрос",
            "user_id": "user_123"
        },
        {
            "content": "Как улучшить маркетинговую стратегию для нашего стартапа?",
            "expected_context": "профессиональный",
            "expected_intent": "вопрос",
            "user_id": "user_456"
        },
        {
            "content": "Интересный факт: 80% успешных людей медитируют каждый день.",
            "expected_context": "общий",
            "expected_intent": "наблюдение",
            "user_id": "user_789"
        },
        {
            "content": "Помогите! У нас кризис на проекте, все сроки горят!",
            "expected_context": "кризисный",
            "expected_intent": "кризис",
            "user_id": "user_123"  # Same user to test history
        },
        {
            "content": "Я хочу улучшить свои навыки в машинном обучении и искусственном интеллекте, особенно в области обработки естественного языка. Также интересуюсь последними трендами в глубоком обучении и нейронных сетях.",
            "expected_context": "профессиональный",  # Note: This test case is primarily for topic analysis
            "expected_intent": "задача",  # Note: This test case is primarily for topic analysis
            "user_id": "user_789"
        }
    ]

    print("Testing Reflection Agent...")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {test_case['content']}")
        print(f"User: {test_case.get('user_id', 'unknown')}")

        # Create input
        input_data = ReflectionInput(
            content=test_case['content'],
            user_id=test_case.get('user_id')
        )

        # Run analysis
        result = agent.reflect(input_data)

        print(f"Context: {result.context} (Expected: {test_case['expected_context']})")
        print(f"Intent: {result.intent} (Expected: {test_case['expected_intent']})")
        print(f"User ID: {result.user_id}")
        print(f"Domain Tags: {result.domain_tags}")
        print(f"Recommended Agents: {result.recommended_agents}")
        print(f"Next Agent: {result.next_agent}")
        print(f"Priority: {result.priority}")
        print(f"Reasoning: {result.reasoning}")
        print(f"Sentiment: {result.sentiment} (Score: {result.sentiment_score:.2f})")
        if result.emotion_details:
            print(f"Emotion Details: {result.emotion_details}")
        print(f"Topics: {result.topics}")
        if result.topic_distribution:
            print(f"Topic Distribution: {result.topic_distribution}")
        if result.subtopics:
            print(f"Subtopics: {result.subtopics}")
        if result.topic_keywords:
            print(f"Topic Keywords: {result.topic_keywords}")
        print(f"Temporal Patterns: {result.temporal_patterns}")

        # Check if context and intent match expected
        context_correct = result.context == test_case['expected_context']
        intent_correct = result.intent == test_case['expected_intent']
        user_correct = result.user_id == test_case.get('user_id')

        if context_correct and intent_correct and user_correct:
            print("✅ Context, intent, and user classification correct")
        elif context_correct and intent_correct:
            print("✅ Context and intent classification correct, ❌ user ID incorrect")
        elif context_correct:
            print("✅ Context classification correct, ❌ intent or user ID incorrect")
        elif intent_correct:
            print("❌ Context classification incorrect, ✅ intent correct")
        else:
            print("❌ Context, intent, or user classification incorrect")

        print("-" * 30)

    print("\nAll tests completed!")

if __name__ == "__main__":
    test_reflection_agent()





