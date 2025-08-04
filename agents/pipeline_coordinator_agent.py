
"""
PipelineCoordinatorAgent - Unified agent that combines routing, aggregation, and pipeline coordination.

This agent replaces both AggregatorAgent and Router, providing comprehensive pipeline management.
"""

from typing import Dict, Any, Union, List, Optional, Literal
from pydantic import BaseModel
from memory.weaviate_client import WeaviateMemory
from .analyzers.context_classifier import ContextClassifier, ContextAnalysis
from .analyzers.intent_identifier import IntentIdentifier, IntentAnalysis
from .analyzers.pattern_matcher import PatternMatcher, PatternAnalysis
from .reflection.document_reflection_agent import DocumentReflectionAgent

class RoutingDecision(BaseModel):
    """Decision on how to route the input data"""
    next_agent: str
    priority: Literal['high', 'medium', 'low']
    reasoning: str
    context_analysis: ContextAnalysis
    intent_analysis: IntentAnalysis
    pattern_analysis: PatternAnalysis

class PipelineCoordinatorAgent:
    """
    Unified agent that combines routing, aggregation, and pipeline coordination.
    Replaces both AggregatorAgent and Router.
    """

    def __init__(self, memory: Optional[WeaviateMemory] = None):
        """
        Initialize PipelineCoordinatorAgent with all required components.
        """
        # Initialize memory and analyzers
        self.memory = memory or WeaviateMemory()
        self.context_classifier = ContextClassifier()
        self.intent_identifier = IntentIdentifier()
        self.pattern_matcher = PatternMatcher(memory=self.memory)

        # Reflection and analysis
        self.document_reflector = DocumentReflectionAgent()

        # Initialize router components
        self.router_components = {
            'context_classifier': self.context_classifier,
            'intent_identifier': self.intent_identifier,
            'pattern_matcher': self.pattern_matcher
        }

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
        agent_name = self.simple_route_text(cleaned_text)

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

    def analyze_and_route(self, text: str) -> RoutingDecision:
        """
        Perform comprehensive analysis and determine routing.

        Args:
            text: Input text to analyze

        Returns:
            RoutingDecision with routing information
        """
        # Perform all analyses
        context_analysis = self.context_classifier.classify(text)
        intent_analysis = self.intent_identifier.identify(text)
        pattern_analysis = self.pattern_matcher.analyze_patterns(text)

        # Determine next agent based on analysis
        next_agent, priority, reasoning = self._determine_routing(
            context_analysis,
            intent_analysis,
            pattern_analysis
        )

        return RoutingDecision(
            next_agent=next_agent,
            priority=priority,
            reasoning=reasoning,
            context_analysis=context_analysis,
            intent_analysis=intent_analysis,
            pattern_analysis=pattern_analysis
        )

    def _determine_routing(self, context_analysis: ContextAnalysis,
                          intent_analysis: IntentAnalysis,
                          pattern_analysis: PatternAnalysis) -> tuple:
        """
        Determine routing based on analysis results.

        Args:
            context_analysis: Context classification results
            intent_analysis: Intent identification results
            pattern_analysis: Pattern matching results

        Returns:
            Tuple of (next_agent, priority, reasoning)
        """
        # Base routing logic
        if intent_analysis.intent_type == 'вопрос':
            if context_analysis.context == 'профессиональный':
                next_agent = 'BusinessAnalysisAgent'
                priority = 'high'
            else:
                next_agent = 'GeneralQAAgent'
                priority = 'medium'
        elif intent_analysis.intent_type == 'задача':
            next_agent = 'TaskPlannerAgent'
            priority = 'high'
        elif intent_analysis.intent_type == 'кризисный':
            next_agent = 'CrisisManagementAgent'
            priority = 'high'
        else:
            next_agent = 'GeneralAnalysisAgent'
            priority = 'medium'

        # Adjust based on patterns
        if pattern_analysis.is_repeated:
            next_agent = 'PatternHandlerAgent'
            priority = 'medium'
            reasoning = f"Обнаружен повторяющийся паттерн. Перенаправляю к специализированному обработчику."
        else:
            reasoning = f"На основе анализа контекста ({context_analysis.context}) и намерения ({intent_analysis.intent_type})"

        return next_agent, priority, reasoning

    def simple_route_text(self, text: str) -> str:
        """
        Simple placeholder for routing logic.

        Args:
            text: Input text to route

        Returns:
            Agent name for processing
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
    # Create coordinator
    coordinator = PipelineCoordinatorAgent()

    # Test with text input
    test_text = """
    Настоящий договор аренды заключён между ООО "Ромашка" и ИП Иванов И.И.
    Сумма аренды: 50000 руб. в месяц. Срок: с 15.07.2023 по 15.07.2024.
    Контактный телефон: 8 (495) 123-45-67, email: contact@romashka.ru
    """

    print("Processing text document...")
    result = coordinator.process("text", test_text)
    print(f"Cleaned text: {result['cleaned_text'][:100]}...")
    print(f"Agent name: {result['agent_name']}")
    print(f"Reflection results summary: {result['reflection_results']['summary']['summary']}")

    # Test routing
    print("\nTesting routing...")
    routing_result = coordinator.analyze_and_route(test_text)
    print(f"Next agent: {routing_result.next_agent}")
    print(f"Priority: {routing_result.priority}")
    print(f"Reasoning: {routing_result.reasoning}")
