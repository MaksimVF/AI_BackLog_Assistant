




"""
Test script for ReflectionAgent with contradiction detection.
"""

from agents.reflection import ReflectionAgent

def test_reflection_with_contradictions():
    """Test the ReflectionAgent with data containing contradictions."""

    # Create the ReflectionAgent
    agent = ReflectionAgent()
    print("✅ ReflectionAgent initialized successfully")

    # Sample data with contradictions
    sample_data = {
        "text": "This contract starts on 2023-12-01 and ends on 2023-01-01. "
                "It mentions no VAT but includes a VAT amount of 1000.",
        "start_date": "2023-12-01",
        "end_date": "2023-01-01",
        "tax_info": "без НДС",
        "vat_amount": 1000,
        "payment_terms": "free of charge",
        "total_amount": 5000,
        "text_coverage": 0.8,
        "ocr_quality": 0.9
    }

    # Sample metadata
    sample_metadata = {
        "data_type": "contract",
        "source": "uploaded_pdf"
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
        if "contradictions" in rec:
            for j, contradiction in enumerate(rec["contradictions"]):
                print(f"     - {contradiction['issue']} ({contradiction['fields']})")

    # Show agent status
    print(f"\n🔧 Agent Status:")
    status = agent.get_status()
    for agent_name, agent_status in status.items():
        print(f"  {agent_name}: {agent_status.get('status', 'unknown')}")

if __name__ == "__main__":
    test_reflection_with_contradictions()




