




"""
Test script for the DocumentReflectionAgent.
"""

from agents.reflection import DocumentReflectionAgent

def test_document_reflection_agent():
    print("Testing DocumentReflectionAgent...")

    # Create the agent
    agent = DocumentReflectionAgent()

    # Test data
    document_text = """
    В соответствии с настоящим договором, стороны обязуются выполнить работы
    в установленные сроки и согласно утвержденному плану. Договор вступает в силу
    с момента подписания и действует до 31 декабря 2025 года.
    """

    text_blocks = [
        "В соответствии с настоящим договором, стороны обязуются выполнить работы",
        "В соответствии с настоящим договором, стороны обязуются выполнить работы",  # Duplicate
        "Договор вступает в силу с момента подписания",
        "Договор действует до 31 декабря 2025 года"
    ]

    structured_data = {
        "document_title": "Contract Agreement",
        "document_type": "contract",
        "date_created": "2024-01-01",
        "counterparty_name": "Company LLC",
        "signatory": "John Doe",
        "jurisdiction": "Russia",
        "effective_date": "2024-01-01",
        "termination_date": "2025-12-31",
        "terms": "Standard terms apply",
        "obligations": {
            "Party A": "Party A обязуется выполнить работы",
            "Party B": "Party B обязуется оплатить услуги"
        },
        "termination": "30 days notice",
        "signatures": "Signed by both parties"
    }

    print("1. Testing text analysis...")
    text_results = agent.analyze_text(document_text, text_blocks)
    print(f"Summary: {text_results['summary']['summary']}")
    print(f"Sentiment analysis: {text_results['sentiment_analysis']['sentiment_analysis']}")
    print(f"Style analysis tone: {text_results['style_analysis']['tone']}")
    print(f"Fact verification: {text_results['fact_verification']['verification_results'][0]}")
    print(f"Ambiguity detected: {text_results['ambiguity_detection']['ambiguity_detected']}")
    print(f"Conflict detected: {text_results['conflict_detection']['conflict_detected']}")
    print(f"Redundancy found: {text_results['redundancy_analysis']['redundant_blocks_found']}")
    print()

    print("2. Testing structure analysis...")
    structure_results = agent.analyze_structure(structured_data)
    print(f"Missing fields: {structure_results['gap_analysis']['missing_fields']}")
    print(f"Semantic consistency: {structure_results['semantic_consistency']['is_complete']}")
    print(f"Recommendation: {structure_results['semantic_consistency']['recommendation']}")
    print()

    print("3. Testing comprehensive analysis...")
    comprehensive_results = agent.comprehensive_analysis(document_text, structured_data, text_blocks)
    print(f"Overall issues found: {comprehensive_results['overall_status']['issues_found']}")
    print(f"Overall recommendation: {comprehensive_results['overall_status']['recommendation']}")
    print()

if __name__ == "__main__":
    test_document_reflection_agent()



