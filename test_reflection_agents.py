

"""
Test script for the new reflection agents.
"""

from agents.reflection import (
    GapDetector,
    RedundancyDetector,
    AmbiguityDetector,
    ConflictDetector,
    StyleAndToneAnalyzer
)

def test_gap_detector():
    print("Testing GapDetector...")
    detector = GapDetector()

    # Test with missing fields
    incomplete_data = {
        "document_title": "Contract",
        "document_type": "Agreement",
        # Missing date_created, counterparty_name, signatory, jurisdiction
    }

    result = detector.evaluate(incomplete_data)
    print(f"Missing fields found: {result['missing_fields_found']}")
    print(f"Missing fields: {result['missing_fields']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

    # Test with complete data
    complete_data = {
        "document_title": "Contract",
        "document_type": "Agreement",
        "date_created": "2023-01-01",
        "counterparty_name": "ABC Corp",
        "signatory": "John Doe",
        "jurisdiction": "USA"
    }

    result = detector.evaluate(complete_data)
    print(f"Missing fields found: {result['missing_fields_found']}")
    print(f"Missing fields: {result['missing_fields']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

def test_redundancy_detector():
    print("Testing RedundancyDetector...")
    detector = RedundancyDetector(repetition_threshold=2)

    # Test with redundant blocks
    text_blocks = [
        "This is a contract between Party A and Party B",
        "Party A agrees to provide services",
        "Party B agrees to pay for services",
        "This is a contract between Party A and Party B",  # Duplicate
        "Party A agrees to provide services",  # Duplicate
        "Additional terms may apply"
    ]

    result = detector.evaluate(text_blocks)
    print(f"Redundant blocks found: {result['redundant_blocks_found']}")
    print(f"Redundant blocks: {result['redundant_blocks']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

def test_ambiguity_detector():
    print("Testing AmbiguityDetector...")
    detector = AmbiguityDetector()

    # Test with ambiguous text
    ambiguous_text = """
    Стороны обязуются выполнить работы в разумный срок.
    В исключительных случаях сроки могут быть изменены по усмотрению заказчика.
    """

    result = detector.evaluate(ambiguous_text)
    print(f"Ambiguity detected: {result['ambiguity_detected']}")
    print(f"Ambiguous phrases: {result['ambiguous_phrases']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

def test_conflict_detector():
    print("Testing ConflictDetector...")
    detector = ConflictDetector()

    # Test with conflicting text
    conflict_text = """
    Работы должны быть выполнены не позднее 30 дней с момента подписания договора.
    Однако, в некоторых случаях работы могут быть начаты не ранее 45 дней после подписания.
    """

    result = detector.evaluate(conflict_text)
    print(f"Conflict detected: {result['conflict_detected']}")
    print(f"Conflict descriptions: {result['conflict_descriptions']}")
    print(f"Recommendation: {result['recommendation']}")
    print()

def test_style_and_tone_analyzer():
    print("Testing StyleAndToneAnalyzer...")
    analyzer = StyleAndToneAnalyzer()

    # Test with informal text
    informal_text = """
    Привет, друзья! Короче, мы тут собрались и решили, что надо сделать вот это дело.
    Типо, все должны подойти и помочь, а то не успеем.
    """

    result = analyzer.analyze(informal_text)
    print(f"Tone: {result['tone']}")
    print(f"Official phrases found: {result['official_phrases_found']}")
    print(f"Informal phrases found: {result['informal_phrases_found']}")
    print(f"Issues: {result['issues']}")
    print()

    # Test with formal text
    formal_text = """
    В соответствии с настоящим договором, стороны обязуются выполнить работы
    в установленные сроки и согласно утвержденному плану.
    """

    result = analyzer.analyze(formal_text)
    print(f"Tone: {result['tone']}")
    print(f"Official phrases found: {result['official_phrases_found']}")
    print(f"Informal phrases found: {result['informal_phrases_found']}")
    print(f"Issues: {result['issues']}")
    print()

if __name__ == "__main__":
    test_gap_detector()
    test_redundancy_detector()
    test_ambiguity_detector()
    test_conflict_detector()
    test_style_and_tone_analyzer()

