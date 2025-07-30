

# agents/reflection/reflection_agent.py

"""
ReflectionAgent - Core intelligent agent for cognitive analysis and pipeline optimization.

This agent coordinates multiple sub-agents to evaluate data completeness, resolve ambiguities,
adjust processing pipelines, refine queries, and build hypotheses.
"""

from .completeness_evaluator import CompletenessEvaluator
from .ambiguity_resolver import AmbiguityResolver
from .pipeline_adjuster import PipelineAdjuster
from .query_refiner import QueryRefiner
from .hypothesis_builder import HypothesisBuilder
from .reasoning_orchestrator import ReasoningOrchestrator

class ReflectionAgent:
    def __init__(self):
        """
        Initialize ReflectionAgent with all sub-agents.
        """
        self.completeness_evaluator = CompletenessEvaluator()
        self.ambiguity_resolver = AmbiguityResolver()
        self.pipeline_adjuster = PipelineAdjuster()
        self.query_refiner = QueryRefiner()
        self.hypothesis_builder = HypothesisBuilder()

        # Initialize orchestrator with all sub-agents
        self.orchestrator = ReasoningOrchestrator(
            evaluators=[
                self.completeness_evaluator,
                self.ambiguity_resolver,
                self.pipeline_adjuster,
                self.query_refiner,
                self.hypothesis_builder
            ]
        )

    def reflect(self, structured_data: dict, metadata: dict = None) -> dict:
        """
        Conducts reflective analysis based on previously extracted data.

        Args:
            structured_data: Structured data from previous agents
            metadata: Additional metadata (optional)

        Returns:
            Dictionary with reflection results including:
            - completeness_score
            - ambiguities
            - pipeline_adjustments
            - refined_queries
            - hypotheses
            - recommendations
        """
        return self.orchestrator.run(structured_data, metadata)

    def get_status(self) -> dict:
        """
        Get the current status of all sub-agents.

        Returns:
            Dictionary with status information from each sub-agent
        """
        return {
            "completeness_evaluator": self.completeness_evaluator.get_status(),
            "ambiguity_resolver": self.ambiguity_resolver.get_status(),
            "pipeline_adjuster": self.pipeline_adjuster.get_status(),
            "query_refiner": self.query_refiner.get_status(),
            "hypothesis_builder": self.hypothesis_builder.get_status(),
            "orchestrator": self.orchestrator.get_status()
        }

