from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from crewai import Agent, Task
from memory.weaviate_client import WeaviateMemory
import json

class ReflectionInput(BaseModel):
    """Input schema for Reflection Agent"""
    text: str  # The main text content to analyze
    metadata: Optional[Dict] = Field(default_factory=dict)  # Additional metadata
    context: Optional[str] = None  # Optional context information

class ReflectionOutput(BaseModel):
    """Output schema for Reflection Agent"""
    context_category: str  # Context category (personal growth, business, IT, etc.)
    required_agents: List[str]  # List of agent types required for processing
    novelty_score: float  # Novelty score (0-1) where 1 is completely new
    complexity_level: str  # Complexity level (low, medium, high)
    user_goals: List[str]  # Identified user goals
    analysis_summary: str  # Summary of the analysis
    similar_cases: Optional[List[Dict]] = None  # Similar cases from memory

class ReflectionAgent(Agent):
    """Agent that performs deep analysis of input data to determine context, required agents, and novelty"""

    def __init__(self, memory: Optional[WeaviateMemory] = None):
        super().__init__(
            name="ReflectionAgent",
            description="Performs deep analysis of input data to determine context, required agents, and novelty",
            input_schema=ReflectionInput,
            output_schema=ReflectionOutput
        )
        self.memory = memory or WeaviateMemory()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Perform text analysis to extract meaning, category, and complexity

        Args:
            text: Input text to analyze

        Returns:
            Dictionary with analysis results
        """
        # In a real implementation, this would use NLP models
        # For now, we'll use simple heuristics

        # Determine context category
        categories = ['personal growth', 'business', 'IT', 'education', 'health', 'finance']
        category_scores = {cat: text.lower().count(cat) for cat in categories}
        context_category = max(category_scores.items(), key=lambda x: x[1])[0]

        # Determine complexity (simple heuristic based on length and special terms)
        word_count = len(text.split())
        special_terms = ['strategy', 'implementation', 'architecture', 'optimization', 'transformation']
        complexity_score = sum(text.lower().count(term) for term in special_terms) + (word_count // 100)

        if complexity_score > 5:
            complexity_level = 'high'
        elif complexity_score > 2:
            complexity_level = 'medium'
        else:
            complexity_level = 'low'

        # Extract potential user goals
        goal_keywords = ['achieve', 'improve', 'learn', 'develop', 'optimize', 'solve', 'create']
        user_goals = []
        for keyword in goal_keywords:
            if keyword in text.lower():
                # Extract sentence containing the keyword
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        user_goals.append(sentence.strip())
                        break

        return {
            'context_category': context_category,
            'complexity_level': complexity_level,
            'user_goals': user_goals,
            'complexity_score': complexity_score
        }

    def determine_required_agents(self, context_category: str, complexity_level: str) -> List[str]:
        """
        Determine which agents are needed based on context and complexity

        Args:
            context_category: The identified context category
            complexity_level: The identified complexity level

        Returns:
            List of required agent types
        """
        # Base agents for all contexts
        base_agents = ['AnalysisAgent', 'CategorizationAgent']

        # Context-specific agents
        context_agents = {
            'personal growth': ['PersonalGrowthAgent', 'GoalSettingAgent'],
            'business': ['BusinessAnalysisAgent', 'DecisionMakingAgent'],
            'IT': ['TechnicalAnalysisAgent', 'ArchitectureAgent'],
            'education': ['LearningAgent', 'ContentRecommendationAgent'],
            'health': ['HealthAnalysisAgent', 'WellnessAgent'],
            'finance': ['FinancialAnalysisAgent', 'InvestmentAgent']
        }

        # Complexity-based agents
        complexity_agents = {
            'low': ['SimpleProcessingAgent'],
            'medium': ['MediumProcessingAgent', 'VisualizationAgent'],
            'high': ['AdvancedProcessingAgent', 'VisualizationAgent', 'DecisionSupportAgent']
        }

        return base_agents + context_agents.get(context_category, []) + complexity_agents.get(complexity_level, [])

    def assess_novelty(self, text: str) -> float:
        """
        Assess the novelty of the request by searching memory for similar cases

        Args:
            text: Input text to assess

        Returns:
            Novelty score between 0 (not novel) and 1 (completely novel)
        """
        # Query memory for similar cases
        similar_cases = self.memory.query_similar(text, limit=5)

        # Calculate similarity score (simple heuristic)
        if not similar_cases:
            return 1.0  # Completely novel

        # In a real implementation, we'd use proper similarity metrics
        # For now, we'll use a simple count-based approach
        similarity_score = min(len(similar_cases) / 5, 1.0)
        return 1.0 - similarity_score  # Higher means more novel

    def execute(self, input_data: ReflectionInput) -> ReflectionOutput:
        """
        Execute the reflection analysis process

        Args:
            input_data: The input data to analyze

        Returns:
            ReflectionOutput: Complete analysis results
        """
        # Perform text analysis
        text_analysis = self.analyze_text(input_data.text)

        # Determine required agents
        required_agents = self.determine_required_agents(
            text_analysis['context_category'],
            text_analysis['complexity_level']
        )

        # Assess novelty
        novelty_score = self.assess_novelty(input_data.text)

        # Get similar cases from memory
        similar_cases = self.memory.query_similar(input_data.text, limit=3)

        # Create output
        return ReflectionOutput(
            context_category=text_analysis['context_category'],
            required_agents=required_agents,
            novelty_score=novelty_score,
            complexity_level=text_analysis['complexity_level'],
            user_goals=text_analysis['user_goals'],
            analysis_summary=(
                f"Analyzed text about {text_analysis['context_category']} with "
                f"{text_analysis['complexity_level']} complexity. "
                f"Novelty score: {novelty_score:.2f}. "
                f"Identified {len(text_analysis['user_goals'])} user goals."
            ),
            similar_cases=similar_cases
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
