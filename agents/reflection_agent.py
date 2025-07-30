




from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field
from crewai import Agent, Task
from memory.weaviate_client import WeaviateMemory
from .analyzers.context_classifier import ContextClassifier, ContextAnalysis
from .analyzers.intent_identifier import IntentIdentifier, IntentAnalysis

from .analyzers.pattern_matcher import PatternMatcher, PatternAnalysis
from .analyzers.sentiment_analyzer import SentimentAnalyzer, SentimentAnalysis
from .analyzers.temporal_analyzer import TemporalAnalyzer, TemporalPattern
from .analyzers.topic_modeler import TopicModeler, TopicAnalysis

from .router import Router, RoutingDecision
import json
import logging

logger = logging.getLogger(__name__)

class ReflectionInput(BaseModel):
    """Input schema for Reflection Agent"""
    content: str  # The main content to analyze
    metadata: Dict = Field(default_factory=dict)  # Additional metadata
    user_id: Optional[str] = None  # User identifier for personalized analysis

class ReflectionOutput(BaseModel):
    """Output schema for Reflection Agent"""
    context: Literal['личный', 'профессиональный', 'кризисный', 'общий', 'неизвестно']
    intent: Literal['вопрос', 'задача', 'наблюдение', 'опыт', 'вывод', 'размышление', 'кризис', 'неизвестно']
    domain_tags: List[str]
    recommended_agents: List[str]  # List of recommended agent types
    reasoning: str  # Reasoning behind the analysis
    similarity_case_id: Optional[str] = None  # ID of similar case if found
    is_repeated_pattern: bool = False  # Whether this is a repeated pattern
    next_agent: str  # Next agent to route to
    priority: Literal['high', 'medium', 'low']  # Processing priority
    user_id: Optional[str] = None  # User identifier

    # New analysis fields
    sentiment: Optional[str] = None  # Sentiment analysis result
    sentiment_score: Optional[float] = None  # Sentiment score (-1 to 1)
    emotion_details: Optional[dict] = None  # Detailed emotion analysis
    topics: Optional[List[str]] = None  # Detected topics
    topic_distribution: Optional[Dict[str, float]] = None  # Topic distribution
    subtopics: Optional[Dict[str, List[str]]] = None  # Subtopics for each main topic
    topic_keywords: Optional[Dict[str, List[str]]] = None  # Key keywords for each topic
    temporal_patterns: Optional[List[str]] = None  # Detected temporal patterns

class ReflectionAgent(Agent):
    """Agent that performs deep analysis of input data to determine context, required agents, and novelty"""

    def __init__(self, memory: Optional[WeaviateMemory] = None, user_id: Optional[str] = None, **kwargs):
        # Initialize CrewAI Agent with our custom properties
        super().__init__(
            role="Reflection Analyst",
            goal="Понять суть входной информации, определить тип данных и требуемые этапы обработки",
            backstory="Ты искусственный специалист, который классифицирует ввод пользователя и выстраивает стратегию анализа.",
            tools=[],  # позже можно подключить tool для Weaviate
            allow_delegation=False,
            **kwargs
        )
        # Store memory separately to avoid CrewAI validation
        object.__setattr__(self, 'memory', memory or WeaviateMemory())
        object.__setattr__(self, 'router', Router(memory=self.memory))
        object.__setattr__(self, 'context_classifier', ContextClassifier())
        object.__setattr__(self, 'intent_identifier', IntentIdentifier())
        object.__setattr__(self, 'pattern_matcher', PatternMatcher(memory=self.memory))
        object.__setattr__(self, 'sentiment_analyzer', SentimentAnalyzer())
        object.__setattr__(self, 'temporal_analyzer', TemporalAnalyzer(memory=self.memory))
        object.__setattr__(self, 'topic_modeler', TopicModeler())
        object.__setattr__(self, 'user_id', user_id)

        # Fetch user history if available
        if self.user_id:
            object.__setattr__(self, 'user_history', self._fetch_user_history())
        else:
            object.__setattr__(self, 'user_history', [])

    def _fetch_user_history(self) -> List[Dict[str, Any]]:
        """Fetch user history from memory"""
        if not self.user_id:
            return []

        try:
            # Fetch user-specific history from Weaviate
            history = self.memory.query_similar_cases(f"user:{self.user_id}", limit=10)
            logger.info(f"Fetched history for user {self.user_id}: {len(history)} items")
            return history
        except Exception as e:
            logger.error(f"Error fetching user history: {e}")
            return []

    def reflect(self, input_data: ReflectionInput) -> ReflectionOutput:
        """
        Main reflection method that analyzes input and determines next steps

        Args:
            input_data: The input data to analyze

        Returns:
            ReflectionOutput: Complete analysis results
        """
        logger.info(f"[ReflectionAgent] Analyzing input for user {input_data.user_id or 'unknown'}")

        # Perform content analysis
        content_analysis = self.analyze_content(input_data.content)

        # Determine recommended agents
        recommended_agents = self.determine_recommended_agents(
            content_analysis['context'],
            content_analysis['intent'],
            content_analysis['domain_tags']
        )

        # Get routing decision
        routing_decision = self.router.analyze_and_route(input_data.content)

        # Find similar case using Weaviate
        similarity_case_id = self.memory.find_similar_case(input_data.content)

        # Store the current case in memory for future reference
        case_id = f"case_{hash(input_data.content)}"
        self.memory.store_case(
            case_id=case_id,
            content=input_data.content,
            context=content_analysis['context'],
            domain_tags=content_analysis['domain_tags'],
            metadata=input_data.metadata,
            user_id=input_data.user_id
        )

        # Create output
        return ReflectionOutput(
            context=content_analysis['context'],
            intent=content_analysis['intent'],
            domain_tags=content_analysis['domain_tags'],
            recommended_agents=recommended_agents,
            reasoning=content_analysis['reasoning'],
            similarity_case_id=similarity_case_id,
            is_repeated_pattern=content_analysis['pattern_analysis'].is_repeated,
            next_agent=routing_decision.next_agent,
            priority=routing_decision.priority,
            user_id=input_data.user_id,
            sentiment=content_analysis['sentiment_analysis'].sentiment,
            sentiment_score=content_analysis['sentiment_analysis'].sentiment_score,
            emotion_details=content_analysis['sentiment_analysis'].emotion_details,
            topics=content_analysis['topic_analysis'].topics,
            topic_distribution=content_analysis['topic_analysis'].topic_distribution,
            subtopics=content_analysis['topic_analysis'].subtopics,
            topic_keywords=content_analysis['topic_analysis'].keywords,
            temporal_patterns=[p.pattern_type for p in content_analysis['temporal_patterns']]
        )

    def analyze_content(self, content: str) -> Dict[str, Any]:
        """
        Perform comprehensive content analysis using all analyzers

        Args:
            content: Input content to analyze

        Returns:
            Dictionary with analysis results
        """
        # Perform all analyses
        context_analysis = self.context_classifier.classify(content)
        intent_analysis = self.intent_identifier.identify(content)
        pattern_analysis = self.pattern_matcher.analyze_patterns(content)

        # New analyzers
        sentiment_analysis = self.sentiment_analyzer.analyze(content)
        topic_analysis = self.topic_modeler.analyze_topics(content)

        # Temporal analysis (if user_id is available)
        temporal_patterns = []
        if self.user_id:
            temporal_patterns = self.temporal_analyzer.analyze_patterns(self.user_id, content)

        # Determine domain tags based on context, intent, and topics
        domain_tags = self._generate_domain_tags(context_analysis.context, intent_analysis.intent_type)
        domain_tags.extend(topic_analysis.topics)

        # Generate comprehensive reasoning
        reasoning = (
            f"Контекст: {context_analysis.context} ({context_analysis.confidence:.2f}). "
            f"Намерение: {intent_analysis.intent_type} ({intent_analysis.confidence:.2f}). "
            f"Сентимент: {sentiment_analysis.sentiment} ({sentiment_analysis.sentiment_score:.2f}). "
            f"Основные темы: {', '.join(domain_tags)}. "
        )

        if pattern_analysis.is_repeated:
            reasoning += f"Обнаружен повторяющийся паттерн: {pattern_analysis.pattern_description}. "

        if temporal_patterns:
            reasoning += f"Временные паттерны: {', '.join(p.pattern_type for p in temporal_patterns)}. "

        return {
            'context': context_analysis.context,
            'intent': intent_analysis.intent_type,
            'domain_tags': domain_tags,
            'reasoning': reasoning,
            'pattern_analysis': pattern_analysis,
            'sentiment_analysis': sentiment_analysis,
            'topic_analysis': topic_analysis,
            'temporal_patterns': temporal_patterns
        }

    def _generate_domain_tags(self, context: str, intent: str) -> List[str]:
        """
        Generate domain tags based on context and intent

        Args:
            context: The identified context
            intent: The identified intent

        Returns:
            List of domain tags
        """
        domain_tags = []

        # Context-based tags
        context_tags = {
            'личный': ['мотивация', 'саморазвитие', 'эмоции'],
            'профессиональный': ['карьера', 'проекты', 'коммуникация'],
            'кризисный': ['стресс', 'решение проблем', 'поддержка'],
            'общий': ['информация', 'знания', 'советы']
        }
        domain_tags.extend(context_tags.get(context, []))

        # Intent-based tags
        intent_tags = {
            'вопрос': ['поиск ответа', 'любопытство'],
            'задача': ['планирование', 'исполнение'],
            'наблюдение': ['анализ', 'данные'],
            'опыт': ['личный опыт', 'примеры'],
            'вывод': ['логика', 'конклюзия'],
            'размышление': ['идеи', 'теории'],
            'кризис': ['срочность', 'проблема', 'помощь']
        }
        domain_tags.extend(intent_tags.get(intent, []))

        return list(set(domain_tags))

    def determine_recommended_agents(self, context: str, intent: str, domain_tags: List[str]) -> List[str]:
        """
        Determine which agents are recommended based on context, intent and domain tags

        Args:
            context: The identified context
            intent: The identified intent
            domain_tags: The identified domain tags

        Returns:
            List of recommended agent types
        """
        # Base agents for all contexts
        base_agents = ['CategorizationAgent']

        # Context-specific agents
        context_agents = {
            'личный': ['PersonalGrowthAgent', 'EmotionSupportAgent'],
            'профессиональный': ['BusinessAnalysisAgent', 'CareerCoachAgent'],
            'кризисный': ['CrisisManagementAgent', 'SupportAgent'],
            'общий': ['GeneralQAAgent', 'InformationAgent'],
            'неизвестно': ['GeneralAnalysisAgent']
        }

        # Intent-specific agents
        intent_agents = {
            'вопрос': ['QAAgent', 'ResearchAgent'],
            'задача': ['TaskPlannerAgent', 'ExecutionAgent'],
            'наблюдение': ['DataAnalysisAgent', 'InsightAgent'],
            'опыт': ['ExperienceAgent', 'StorytellingAgent'],
            'вывод': ['LogicAgent', 'ConclusionAgent'],
            'размышление': ['IdeaAgent', 'BrainstormingAgent'],
            'кризис': ['CrisisAgent', 'EmergencyAgent']
        }

        # Get agents based on context and intent
        agents = base_agents + context_agents.get(context, []) + intent_agents.get(intent, [])

        # Add domain-specific agents (simplified for this example)
        if 'стресс' in domain_tags:
            agents.append('StressManagementAgent')
        if 'карьера' in domain_tags:
            agents.append('CareerAgent')

        return list(set(agents))  # Remove duplicates

    def execute(self, input_data: ReflectionInput) -> ReflectionOutput:
        """
        Execute the reflection analysis process

        Args:
            input_data: The input data to analyze

        Returns:
            ReflectionOutput: Complete analysis results
        """
        return self.reflect(input_data)

    def run(self, input_data: ReflectionInput) -> ReflectionOutput:
        """
        Alias for execute method to maintain compatibility

        Args:
            input_data: The input data to analyze

        Returns:
            ReflectionOutput: Complete analysis results
        """
        return self.reflect(input_data)

    def process_task(self, task_description: str, input_data: str) -> str:
        """
        Process a task from CrewAI framework

        Args:
            task_description: Description of the task
            input_data: Input data as string (could be JSON)

        Returns:
            JSON string with analysis results
        """
        # Parse input data
        try:
            input_dict = json.loads(input_data)
            reflection_input = ReflectionInput(**input_dict)
        except:
            # Fallback to simple text input
            reflection_input = ReflectionInput(content=input_data)

        # Execute analysis
        result = self.reflect(reflection_input)

        # Convert to JSON string
        return result.json()




