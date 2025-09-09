





"""
AggregatorAgent - Central agent that coordinates the processing pipeline.

This agent integrates input processing, text cleaning, routing, and reflection
to provide comprehensive analysis of input data.
"""

from typing import Dict, Any, Union
# from agents.input_classifier_agent import InputClassifierAgent
# from agents.analyzers.text_cleaner import TextCleaner

# from agents.reflection_agent.contextual_router import route_text

def simple_route_text(text: str) -> str:
    """
    Simple placeholder for routing logic.
    """
    # Basic routing based on keywords
    text_lower = text.lower()
    if "договор" in text_lower or "контракт" in text_lower:
        return "contract_analyzer"
    elif "отчёт" in text_lower or "репорт" in text_lower:
        return "report_analyzer"
    elif "письмо" in text_lower or "email" in text_lower:
        return "email_analyzer"
    else:
        return "general_analyzer"

from agents.reflection.document_reflection_agent import DocumentReflectionAgent

class AggregatorAgent:
    """
    Central agent that coordinates the processing pipeline.
    """

    def __init__(self):
        """
        Initialize AggregatorAgent with all required components.
        """
        # Input processing (placeholder for now)
        # self.input_classifier = InputClassifierAgent()

        # Text processing (placeholder for now)
        # self.text_cleaner = TextCleaner()

        # Reflection and analysis
        self.document_reflector = DocumentReflectionAgent()

    def process(self, input_type: str, data: Union[bytes, str]) -> Dict[str, Any]:
        """
        Process input data through the complete pipeline.

        Args:
            input_type: Type of input ('audio', 'video', 'text', 'image', 'document')
            data: Raw input data (bytes for media, str for text)

        Returns:
            Dictionary with comprehensive processing results
        """
        # Step 1: Input classification and transcription
        if input_type in ['audio', 'video', 'image']:
            # For now, just use placeholder text (InputClassifierAgent not available)
            raw_text = f"Transcribed {input_type} content (placeholder)"
        elif input_type == 'text':
            raw_text = data
        else:
            raise ValueError(f"Unsupported input type: {input_type}")

        # Step 2: Text cleaning (placeholder - just use raw text)
        cleaned_text = raw_text  # Placeholder for text cleaning

        # Step 3: Contextual routing (determine agent type)
        agent_name = simple_route_text(cleaned_text)

        # Step 4: Document reflection and analysis
        reflection_results = self.document_reflector.analyze_text(cleaned_text)

        # Step 5: Aggregate results
        return {
            "input_type": input_type,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "agent_name": agent_name,
            "reflection_results": reflection_results
        }

    def _transcribe_media(self, media_type: str, data: bytes) -> str:
        """
        Transcribe media data to text using InputClassifierAgent.

        Args:
            media_type: Type of media ('audio', 'video', 'image')
            data: Raw media data as bytes

        Returns:
            Transcribed text
        """
        # Use the InputClassifierAgent to process media
        # This is a simplified approach - in a real implementation,
        # we would need to handle the actual transcription process
        if media_type == 'audio':
            # Simulate audio transcription
            return "Transcribed audio text from InputClassifierAgent"
        elif media_type == 'video':
            # Simulate video transcription
            return "Transcribed video text from InputClassifierAgent"
        elif media_type == 'image':
            # Simulate OCR from image
            return "Extracted text from image using InputClassifierAgent"
        else:
            raise ValueError(f"Unsupported media type: {media_type}")

    def process_document(self, text: str, structured_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a document with comprehensive reflection analysis.

        Args:
            text: Document text
            structured_data: Optional structured document data

        Returns:
            Dictionary with comprehensive document analysis
        """
        if structured_data:
            return self.document_reflector.comprehensive_analysis(text, structured_data)
        else:
            return self.document_reflector.analyze_text(text)

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of all components.

        Returns:
            Dictionary with status information
        """
        return {
            "input_classifier": "Ready",
            "text_cleaner": "Ready",
            "document_reflector": "Ready",
            "available_agents": self._get_available_agents()
        }

    def _get_available_agents(self) -> Dict[str, str]:
        """
        Get available agents and their descriptions.

        Returns:
            Dictionary of agent names and descriptions
        """
        # This would integrate with the actual router system
        return {
            "contract_analyzer": "Analyzes legal contracts",
            "report_analyzer": "Analyzes business reports",
            "email_analyzer": "Analyzes email communications",
            "general_analyzer": "General purpose text analyzer"
        }

# Example usage
if __name__ == "__main__":
    # Create aggregator
    aggregator = AggregatorAgent()

    # Test with text input
    test_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    print("Processing text document...")
    result = aggregator.process("text", test_text)
    print(f"Cleaned text: {result['cleaned_text'][:100]}...")
    print(f"Agent name: {result['agent_name']}")
    print(f"Reflection results summary: {result['reflection_results']['summary']['summary']}")
    print(f"Sentiment analysis: {result['reflection_results']['sentiment_analysis']['sentiment_analysis']}")
    print(f"Ambiguity detected: {result['reflection_results']['ambiguity_detection']['ambiguity_detected']}")

    # Test with document analysis
    print("\nProcessing document with structured data...")
    structured_data = {
        "document_title": "Contract Agreement",
        "document_type": "contract",
        "date_created": "2024-01-01",
        "counterparty_name": "Company LLC",
        "signatory": "John Doe",
        "jurisdiction": "Russia"
    }

    doc_result = aggregator.process_document(test_text, structured_data)
    print(f"Overall recommendation: {doc_result['overall_status']['recommendation']}")
    print(f"Issues found: {doc_result['overall_status']['issues_found']}")





