


"""
Test script for the SemanticConsistencyChecker.
"""

from agents.reflection import SemanticConsistencyChecker

def test_semantic_consistency_checker():
    print("Testing SemanticConsistencyChecker...")

    # Test with missing sections
    checker = SemanticConsistencyChecker()

    incomplete_document = {
        "title": "Contract Agreement",
        "parties": "Party A and Party B",
        # Missing effective_date, terms, obligations, termination, signatures
    }

    result = checker.analyze(incomplete_document)
    print("Test 1: Incomplete document")
    print(f"Missing sections: {result['missing_sections']}")
    print(f"Contradictions found: {result['contradictions_found']}")
    print(f"Is complete: {result['is_complete']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

    # Test with complete document but contradictions
    complete_document = {
        "title": "Contract Agreement",
        "parties": "Party A and Party B",
        "effective_date": "2025-01-01",
        "termination_date": "2024-12-31",  # Earlier than effective date
        "terms": "Standard terms apply",
        "obligations": {
            "Party A": "Party A обязуется выполнить работы и не обязан платить",
            "Party B": "Party B обязуется оплатить услуги"
        },
        "termination": "30 days notice",
        "signatures": "Signed by both parties"
    }

    result = checker.analyze(complete_document)
    print("Test 2: Complete document with contradictions")
    print(f"Missing sections: {result['missing_sections']}")
    print(f"Contradictions found: {result['contradictions_found']}")
    print(f"Is complete: {result['is_complete']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

    # Test with perfect document
    perfect_document = {
        "title": "Contract Agreement",
        "parties": "Party A and Party B",
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

    result = checker.analyze(perfect_document)
    print("Test 3: Perfect document")
    print(f"Missing sections: {result['missing_sections']}")
    print(f"Contradictions found: {result['contradictions_found']}")
    print(f"Is complete: {result['is_complete']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

if __name__ == "__main__":
    test_semantic_consistency_checker()


