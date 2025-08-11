

"""
Test script to demonstrate different agents using different LLM models.
"""

from config.agent_config import get_agent_registry, set_default_model_for_agent
from agents.reflection.document_summarizer import DocumentSummarizer
from agents.llm_client import get_available_models

def test_agent_models():
    """Test different agents using different models"""
    print("Available LLM models:", get_available_models())
    print("Registered agents:", get_agent_registry().list_agents())
    print()

    # Create a DocumentSummarizer with default model
    summarizer1 = DocumentSummarizer()
    print(f"Summarizer1 model: {summarizer1.get_model_name()}")
    print()

    # Create a DocumentSummarizer with specific model
    summarizer2 = DocumentSummarizer(model_name="claude-2")
    print(f"Summarizer2 model: {summarizer2.get_model_name()}")
    print()

    # Test summarization with different models
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines,
    in contrast to the natural intelligence displayed by humans and animals.
    Leading AI textbooks define the field as the study of "intelligent agents":
    any device that perceives its environment and takes actions that maximize
    its chance of successfully achieving its goals.
    """

    print("Testing summarization with different models...")
    print()

    # Test with summarizer1 (uses default model)
    result1 = summarizer1.generate_summary(test_text)
    print(f"Summarizer1 result (model: {result1['model_used']}):")
    print(f"Summary: {result1['summary']}")
    print()

    # Test with summarizer2 (uses claude-2 model)
    result2 = summarizer2.generate_summary(test_text)
    print(f"Summarizer2 result (model: {result2['model_used']}):")
    print(f"Summary: {result2['summary']}")
    print()

    # Test overriding model at runtime
    result3 = summarizer1.generate_summary(test_text, model_name="llama-2-7b")
    print(f"Summarizer1 with override (model: {result3['model_used']}):")
    print(f"Summary: {result3['summary']}")
    print()

    # Change default model for agent and test again
    set_default_model_for_agent("DocumentSummarizer", "llama-2-7b")
    summarizer3 = DocumentSummarizer()
    print(f"Summarizer3 model (after config change): {summarizer3.get_model_name()}")
    result4 = summarizer3.generate_summary(test_text)
    print(f"Summarizer3 result (model: {result4['model_used']}):")
    print(f"Summary: {result4['summary']}")

if __name__ == "__main__":
    test_agent_models()

