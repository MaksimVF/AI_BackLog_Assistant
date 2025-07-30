




#!/usr/bin/env python3

"""Test script for Reflection Agent"""

from agents.reflection_agent import ReflectionAgent, ReflectionInput

def test_reflection_agent():
    """Test the Reflection Agent with different inputs"""

    # Create reflection agent with mock memory
    class MockMemory:
        def find_similar_case(self, text):
            return None

        def store_case(self, case_id, content, context, domain_tags, metadata):
            return {}

        def query_similar_cases(self, text, limit=3):
            return []

    agent = ReflectionAgent(memory=MockMemory())

    # Test cases with expected intents
    test_cases = [
        {
            "content": "Я чувствую себя очень подавленно на работе, не знаю как справиться со стрессом.",
            "expected_context": "личный",
            "expected_intent": "вопрос"
        },
        {
            "content": "Как улучшить маркетинговую стратегию для нашего стартапа?",
            "expected_context": "профессиональный",
            "expected_intent": "вопрос"
        },
        {
            "content": "Интересный факт: 80% успешных людей медитируют каждый день.",
            "expected_context": "общий",
            "expected_intent": "наблюдение"
        },
        {
            "content": "Помогите! У нас кризис на проекте, все сроки горят!",
            "expected_context": "кризисный",
            "expected_intent": "кризис"
        }
    ]

    print("Testing Reflection Agent...")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Input: {test_case['content']}")

        # Create input
        input_data = ReflectionInput(content=test_case['content'])

        # Run analysis
        result = agent.execute(input_data)

        print(f"Context: {result.context} (Expected: {test_case['expected_context']})")
        print(f"Intent: {result.intent} (Expected: {test_case['expected_intent']})")
        print(f"Domain Tags: {result.domain_tags}")
        print(f"Recommended Agents: {result.recommended_agents}")
        print(f"Next Agent: {result.next_agent}")
        print(f"Priority: {result.priority}")
        print(f"Reasoning: {result.reasoning}")

        # Check if context and intent match expected
        context_correct = result.context == test_case['expected_context']
        intent_correct = result.intent == test_case['expected_intent']

        if context_correct and intent_correct:
            print("✅ Context and intent classification correct")
        elif context_correct:
            print("✅ Context classification correct, ❌ intent incorrect")
        elif intent_correct:
            print("❌ Context classification incorrect, ✅ intent correct")
        else:
            print("❌ Context and intent classification incorrect")

        print("-" * 30)

    print("\nAll tests completed!")

if __name__ == "__main__":
    test_reflection_agent()




