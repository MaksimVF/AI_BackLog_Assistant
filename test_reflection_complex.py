



"""
Test script for ReflectionAgent with a more complex example.
"""

from agents.reflection import ReflectionAgent

def test_reflection_complex():
    """Test the ReflectionAgent with incomplete contract data."""

    # Create the ReflectionAgent
    agent = ReflectionAgent()
    print("✅ ReflectionAgent initialized successfully")

    # Sample data with missing fields and low quality
    sample_data = {
        "text": "This contract is between Company A and Company B. "
                "It mentions payment terms but lacks signatures and dates. "
                "The document has pronoun references like 'he' and 'they' without clear context.",
        "terms": "Payment within 30 days",
        "text_coverage": 0.5,  # Low coverage
        "ocr_quality": 0.6,    # Low OCR quality
        "audio_quality": 0.65  # Low audio quality
    }

    # Sample metadata
    sample_metadata = {
        "data_type": "contract",
        "source": "scanned_pdf"
    }

    print("\n📄 Sample Data:")
    for key, value in sample_data.items():
        print(f"  {key}: {value}")

    # Run reflection
    print("\n🤖 Running ReflectionAgent...")
    results = agent.reflect(sample_data, sample_metadata)

    # Display results
    print("\n📊 Reflection Results:")

    # Show evaluation results
    for eval_type, eval_results in results["evaluation_results"].items():
        print(f"\n🔹 {eval_type.capitalize()}:")
        for key, value in eval_results.items():
            if isinstance(value, list) and value:
                print(f"  {key}: {len(value)} items")
                for i, item in enumerate(value[:2]):  # Show first 2 items max
                    print(f"    {i+1}. {item}")
                if len(value) > 2:
                    print(f"    ... and {len(value) - 2} more")
            else:
                print(f"  {key}: {value}")

    # Show final recommendations
    print(f"\n💡 Final Recommendations ({len(results['final_recommendations'])}):")
    for i, rec in enumerate(results["final_recommendations"]):
        print(f"  {i+1}. {rec['type']}: {rec['message']}")
        if "recommendations" in rec:
            for j, sub_rec in enumerate(rec["recommendations"]):
                print(f"     - {sub_rec['action']}: {sub_rec['reason']}")

    # Show agent status
    print(f"\n🔧 Agent Status:")
    status = agent.get_status()
    for agent_name, agent_status in status.items():
        print(f"  {agent_name}: {agent_status.get('status', 'unknown')}")

if __name__ == "__main__":
    test_reflection_complex()



