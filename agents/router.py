

from typing import Dict, List, Optional, Literal
from pydantic import BaseModel
from .analyzers.context_classifier import ContextClassifier, ContextAnalysis
from .analyzers.intent_identifier import IntentIdentifier, IntentAnalysis
from .analyzers.pattern_matcher import PatternMatcher, PatternAnalysis
from memory.weaviate_client import WeaviateMemory

class RoutingDecision(BaseModel):
    """Decision on how to route the input data"""
    next_agent: str
    priority: Literal['high', 'medium', 'low']
    reasoning: str
    context_analysis: ContextAnalysis
    intent_analysis: IntentAnalysis
    pattern_analysis: PatternAnalysis

class Router:
    """Routes input data to appropriate agents based on analysis"""

    def __init__(self, memory: Optional[WeaviateMemory] = None):
        self.context_classifier = ContextClassifier()
        self.intent_identifier = IntentIdentifier()
        self.pattern_matcher = PatternMatcher(memory)
        self.memory = memory or WeaviateMemory()

    def analyze_and_route(self, text: str) -> RoutingDecision:
        """
        Perform comprehensive analysis and determine routing

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
        Determine routing based on analysis results

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

    def log_routing_decision(self, decision: RoutingDecision, input_text: str) -> Dict:
        """
        Log the routing decision to memory

        Args:
            decision: The routing decision to log
            input_text: Original input text

        Returns:
            Dictionary with logging results
        """
        # Store routing decision in memory
        case_id = f"routing_{hash(input_text)}"

        return self.memory.store_case(
            case_id=case_id,
            content=input_text,
            context=decision.context_analysis.context,
            domain_tags=[decision.intent_analysis.intent_type],
            metadata={
                'next_agent': decision.next_agent,
                'priority': decision.priority,
                'reasoning': decision.reasoning,
                'pattern_analysis': decision.pattern_analysis.dict()
            }
        )


