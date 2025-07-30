




from agents.analyzers.semantic_router import SemanticRouter

def test_semantic_router():
    router = SemanticRouter()

    # Test case 1: Video source with financial question
    input1 = {
        "user_id": "user123",
        "text": "Как работает эта финансовая система?",
        "source": "video"
    }

    result1 = router.route(input1)
    print("Test Case 1 - Video with Financial Question:")
    print(f"Agents: {result1['agents']}")
    print(f"Reasoning: {result1['reasoning']}")
    print(f"Priority: {result1['priority']}")
    print(f"Context: {result1['metadata']['context']}")
    print(f"Intent: {result1['metadata']['intent']}")
    print("---")

    # Test case 2: Audio source with task
    input2 = {
        "user_id": "user456",
        "text": "Мне нужно сделать отчет к завтра",
        "source": "audio"
    }

    result2 = router.route(input2)
    print("Test Case 2 - Audio with Task:")
    print(f"Agents: {result2['agents']}")
    print(f"Reasoning: {result2['reasoning']}")
    print(f"Priority: {result2['priority']}")
    print("---")

    # Test case 3: Text source with crisis
    input3 = {
        "user_id": "user789",
        "text": "Помогите! У нас кризис!",
        "source": "text"
    }

    result3 = router.route(input3)
    print("Test Case 3 - Text with Crisis:")
    print(f"Agents: {result3['agents']}")
    print(f"Reasoning: {result3['reasoning']}")
    print(f"Priority: {result3['priority']}")
    print("---")

    # Test case 4: Fallback routing
    input4 = {
        "user_id": "user000",
        "source": "unknown"
    }

    result4 = router.route_with_fallback(input4)
    print("Test Case 4 - Fallback Routing:")
    print(f"Agents: {result4['agents']}")
    print(f"Reasoning: {result4['reasoning']}")
    print(f"Priority: {result4['priority']}")
    print("---")

if __name__ == "__main__":
    test_semantic_router()




