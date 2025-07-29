from agents.reflection_agent import ReflectionAgent, ReflectionInput
from memory.weaviate_client import WeaviateMemory
from schemas import VideoData, AudioData, ImageData, DocumentData, TextData

def main():
    # Initialize components
    memory = WeaviateMemory()
    reflection_agent = ReflectionAgent(memory=memory)

    # Example usage
    print("Welcome to the Multi-Agent System!")

    # Create sample text data for reflection agent
    sample_text = """
    I want to improve my business strategy and optimize our marketing campaigns.
    We need to achieve better customer engagement and develop new sales channels.
    The goal is to transform our business model to be more competitive in the market.
    """

    # Process with reflection agent
    input_data = ReflectionInput(
        text=sample_text,
        metadata={"source": "user_input", "timestamp": "2025-07-29T12:00:00Z"}
    )

    result = reflection_agent.execute(input_data)

    print("\nReflection Agent Analysis Results:")
    print(f"Context Category: {result.context_category}")
    print(f"Complexity Level: {result.complexity_level}")
    print(f"Novelty Score: {result.novelty_score:.2f}")
    print(f"Required Agents: {result.required_agents}")
    print(f"User Goals: {result.user_goals}")
    print(f"Analysis Summary: {result.analysis_summary}")

    if result.similar_cases:
        print(f"\nSimilar Cases Found: {len(result.similar_cases)}")
        for i, case in enumerate(result.similar_cases, 1):
            print(f"  {i}. {case.get('content', 'No content')[:100]}...")

    print("\nProcessing complete!")

if __name__ == "__main__":
    main()
