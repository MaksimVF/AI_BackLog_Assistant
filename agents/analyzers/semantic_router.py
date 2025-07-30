



from typing import Dict, List
from .context_classifier import ContextClassifier
from .intent_identifier import IntentIdentifier
from .metadata_builder import MetadataBuilder

class SemanticRouter:
    """
    Enhanced semantic router that combines source-based and content-based routing.

    Features:
    - Source type routing (video, audio, text)
    - Content-based routing (context, intent)
    - Metadata-driven routing
    - Extensible rule system
    """

    def __init__(self):
        # Initialize analyzers
        self.context_classifier = ContextClassifier()
        self.intent_identifier = IntentIdentifier()
        self.metadata_builder = MetadataBuilder()

        # Define routing rules
        self.source_rules = {
            "video": ["video_transcriber", "frame_extractor"],
            "audio": ["audio_transcriber"],
            "text": ["text_cleaner", "entity_extractor"],
            "default": ["text_cleaner"]
        }

        # Content-based routing rules
        self.content_rules = {
            "финансовый": {
                "вопрос": ["financial_qa_agent", "data_retriever"],
                "задача": ["financial_planner", "task_manager"],
                "кризис": ["crisis_manager", "financial_advisor"]
            },
            "юридический": {
                "вопрос": ["legal_qa_agent", "document_retriever"],
                "задача": ["legal_advisor", "contract_manager"],
                "кризис": ["legal_crisis_manager", "compliance_checker"]
            },
            "бытовой": {
                "вопрос": ["general_qa_agent", "knowledge_base"],
                "задача": ["task_planner", "reminder_service"],
                "кризис": ["emergency_service", "support_agent"]
            }
        }

        # Default fallback rules
        self.default_rules = {
            "вопрос": ["general_qa_agent"],
            "задача": ["task_planner"],
            "кризис": ["crisis_manager"],
            "неизвестно": ["general_analysis_agent"]
        }

    def route(self, user_input: Dict) -> Dict:
        """
        Determine routing based on comprehensive analysis

        Args:
            user_input: Dictionary with user input data

        Returns:
            Dictionary with routing information including:
            - agents: List of agent names
            - reasoning: Explanation of routing decision
            - metadata: Full metadata analysis
        """
        # Build comprehensive metadata
        metadata = self.metadata_builder.build_metadata(user_input)
        text = user_input.get("text", "")

        # Determine source-based routing
        source_type = metadata.get("source", "default").lower()
        source_agents = self._get_source_agents(source_type)

        # Determine content-based routing
        context = metadata.get("context", "неизвестно")
        intent = metadata.get("intent", "неизвестно")
        content_agents = self._get_content_agents(context, intent)

        # Combine routing decisions
        all_agents = list(set(source_agents + content_agents))
        reasoning = self._build_reasoning(source_type, context, intent, all_agents)

        return {
            "agents": all_agents,
            "reasoning": reasoning,
            "metadata": metadata,
            "priority": self._determine_priority(intent, context)
        }

    def _get_source_agents(self, source_type: str) -> List[str]:
        """Get agents based on source type"""
        if "video" in source_type:
            return self.source_rules["video"]
        elif "audio" in source_type:
            return self.source_rules["audio"]
        elif "text" in source_type:
            return self.source_rules["text"]
        else:
            return self.source_rules["default"]

    def _get_content_agents(self, context: str, intent: str) -> List[str]:
        """Get agents based on content analysis"""
        if context in self.content_rules and intent in self.content_rules[context]:
            return self.content_rules[context][intent]
        elif intent in self.default_rules:
            return self.default_rules[intent]
        else:
            return self.default_rules["неизвестно"]

    def _build_reasoning(self, source_type: str, context: str, intent: str, agents: List[str]) -> str:
        """Build reasoning explanation"""
        reasoning = f"Маршрутизация на основе: "
        reasoning += f"типа источника ({source_type}), "
        reasoning += f"контекста ({context}), "
        reasoning += f"намерения ({intent}). "
        reasoning += f"Выбранные агенты: {', '.join(agents)}."
        return reasoning

    def _determine_priority(self, intent: str, context: str) -> str:
        """Determine priority based on intent and context"""
        if intent == "кризис" or context == "кризис":
            return "high"
        elif intent == "задача":
            return "high"
        elif intent == "вопрос" and context in ["финансовый", "юридический"]:
            return "medium"
        else:
            return "low"

    def route_with_fallback(self, user_input: Dict) -> Dict:
        """
        Route with fallback to simple source-based routing if analysis fails

        Args:
            user_input: Dictionary with user input data

        Returns:
            Dictionary with routing information
        """
        try:
            return self.route(user_input)
        except Exception as e:
            # Fallback to simple source-based routing
            source_type = user_input.get("source", "default").lower()
            agents = self._get_source_agents(source_type)
            return {
                "agents": agents,
                "reasoning": f"Fallback routing based on source type: {source_type}",
                "metadata": {"source": source_type},
                "priority": "medium"
            }



