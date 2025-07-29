from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field
from crewai import Agent, Task
from memory.weaviate_client import WeaviateMemory
import json

class ReflectionInput(BaseModel):
    """Input schema for Reflection Agent"""
    content: str  # The main content to analyze
    metadata: Dict = Field(default_factory=dict)  # Additional metadata

class ReflectionOutput(BaseModel):
    """Output schema for Reflection Agent"""
    context: Literal['личный рост', 'бизнес', 'психология', 'обучение', 'неизвестно']
    domain_tags: List[str]
    recommended_agents: List[str]  # List of recommended agent types
    reasoning: str  # Reasoning behind the analysis
    similarity_case_id: Optional[str] = None  # ID of similar case if found

class ReflectionAgent(Agent):
    """Agent that performs deep analysis of input data to determine context, required agents, and novelty"""

    def __init__(self, memory: Optional[WeaviateMemory] = None, **kwargs):
        # Initialize CrewAI Agent with our custom properties
        super().__init__(
            role="Reflection Analyst",
            goal="Понять суть входной информации, определить тип данных и требуемые этапы обработки",
            backstory="Ты искусственный специалист, который классифицирует ввод пользователя и выстраивает стратегию анализа.",
            tools=[],  # позже можно подключить tool для Weaviate
            allow_delegation=False,
            **kwargs
        )
        self.memory = memory or WeaviateMemory()

    def analyze_content(self, content: str) -> Dict[str, Any]:
        """
        Perform content analysis to extract meaning, category, and context

        Args:
            content: Input content to analyze

        Returns:
            Dictionary with analysis results
        """
        # Determine context category with Russian labels
        categories = ['личный рост', 'бизнес', 'психология', 'обучение']
        category_scores = {cat: content.lower().count(cat) for cat in categories}
        context = max(category_scores.items(), key=lambda x: x[1])[0]

        if max(category_scores.values()) == 0:
            context = 'неизвестно'

        # Determine domain tags
        domain_tags = []
        if 'бизнес' in context or 'бизнес' in content.lower():
            domain_tags.extend(['маркетинг', 'стратегия', 'финансы'])
        if 'личный рост' in context or 'личный рост' in content.lower():
            domain_tags.extend(['мотивация', 'саморазвитие', 'цели'])
        if 'психология' in context or 'психология' in content.lower():
            domain_tags.extend(['эмоции', 'поведение', 'самопознание'])
        if 'обучение' in context or 'обучение' in content.lower():
            domain_tags.extend(['образование', 'навыки', 'знания'])

        # Generate reasoning
        reasoning = (
            f"Анализ показал, что контент относится к категории '{context}'. "
            f"Основные темы: {', '.join(domain_tags)}. "
            f"Рекомендованные агенты будут помогать с обработкой этого контента."
        )

        return {
            'context': context,
            'domain_tags': domain_tags,
            'reasoning': reasoning
        }

    def determine_recommended_agents(self, context: str, domain_tags: List[str]) -> List[str]:
        """
        Determine which agents are recommended based on context and domain tags

        Args:
            context: The identified context
            domain_tags: The identified domain tags

        Returns:
            List of recommended agent types
        """
        # Base agents for all contexts
        base_agents = ['CategorizationAgent']

        # Context-specific agents
        context_agents = {
            'личный рост': ['PersonalGrowthAgent', 'GoalSettingAgent'],
            'бизнес': ['BusinessAnalysisAgent', 'DecisionAgent'],
            'психология': ['PsychologyAgent', 'EmotionAnalysisAgent'],
            'обучение': ['LearningAgent', 'ContentRecommendationAgent'],
            'неизвестно': ['GeneralAnalysisAgent']
        }

        # Domain-specific agents
        domain_agents = {
            'маркетинг': ['MarketingAgent'],
            'стратегия': ['StrategyAgent'],
            'финансы': ['FinanceAgent'],
            'мотивация': ['MotivationAgent'],
            'саморазвитие': ['SelfDevelopmentAgent'],
            'эмоции': ['EmotionAgent'],
            'образование': ['EducationAgent']
        }

        # Get agents based on context and domains
        agents = base_agents + context_agents.get(context, [])

        # Add domain-specific agents
        for tag in domain_tags:
            if tag in domain_agents:
                agents.extend(domain_agents[tag])

        return list(set(agents))  # Remove duplicates

    def find_similar_case(self, content: str) -> Optional[str]:
        """
        Find similar case in memory

        Args:
            content: Input content to search for

        Returns:
            ID of similar case if found, None otherwise
        """
        # Query memory for similar cases
        similar_cases = self.memory.query_similar(content, limit=1)

        if similar_cases and len(similar_cases) > 0:
            # Return the first similar case ID
            return similar_cases[0].get('id', None)

        return None

    def execute(self, input_data: ReflectionInput) -> ReflectionOutput:
        """
        Execute the reflection analysis process

        Args:
            input_data: The input data to analyze

        Returns:
            ReflectionOutput: Complete analysis results
        """
        # Perform content analysis
        content_analysis = self.analyze_content(input_data.content)

        # Determine recommended agents
        recommended_agents = self.determine_recommended_agents(
            content_analysis['context'],
            content_analysis['domain_tags']
        )

        # Find similar case
        similarity_case_id = self.find_similar_case(input_data.content)

        # Create output
        return ReflectionOutput(
            context=content_analysis['context'],
            domain_tags=content_analysis['domain_tags'],
            recommended_agents=recommended_agents,
            reasoning=content_analysis['reasoning'],
            similarity_case_id=similarity_case_id
        )

    def run(self, input_data: ReflectionInput) -> ReflectionOutput:
        """
        Alias for execute method to maintain compatibility

        Args:
            input_data: The input data to analyze

        Returns:
            ReflectionOutput: Complete analysis results
        """
        return self.execute(input_data)

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
        result = self.execute(reflection_input)

        # Convert to JSON string
        return result.json()
