






"""
ReasoningOrchestrator - Core sub-agent for coordinating reflection logic.

This agent manages the execution order of other sub-agents, collects their outputs,
and generates final recommendations.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ReasoningOrchestrator:
    def __init__(self, evaluators: List[Any] = None):
        """
        Initialize the ReasoningOrchestrator.

        Args:
            evaluators: List of sub-agent evaluators
        """
        self.evaluators = evaluators or []
        self.execution_order = [
            "CompletenessEvaluator",
            "AmbiguityResolver",
            "ContradictionDetector",
            "PipelineAdjuster",
            "QueryRefiner",
            "HypothesisBuilder"
        ]

    def run(self, data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the reflection pipeline.

        Args:
            data: Structured data to analyze
            metadata: Additional metadata (optional)

        Returns:
            Dictionary with comprehensive reflection results
        """
        results = {
            "input_data": data,
            "metadata": metadata or {},
            "evaluation_results": {},
            "final_recommendations": {},
            "status": "processing"
        }

        # Execute each evaluator in order
        for evaluator in self.evaluators:
            try:
                evaluator_name = evaluator.__class__.__name__

                if evaluator_name == "CompletenessEvaluator":
                    eval_results = evaluator.evaluate(data, metadata.get("data_type") if metadata else None)
                    results["evaluation_results"]["completeness"] = eval_results

                elif evaluator_name == "AmbiguityResolver":
                    eval_results = evaluator.resolve(data)
                    results["evaluation_results"]["ambiguities"] = eval_results

                elif evaluator_name == "ContradictionDetector":
                    eval_results = evaluator.evaluate(data)
                    results["evaluation_results"]["contradictions"] = eval_results

                elif evaluator_name == "PipelineAdjuster":
                    eval_results = evaluator.adjust(data, results["evaluation_results"])
                    results["evaluation_results"]["pipeline"] = eval_results

                elif evaluator_name == "QueryRefiner":
                    eval_results = evaluator.refine(data, results["evaluation_results"])
                    results["evaluation_results"]["queries"] = eval_results

                elif evaluator_name == "HypothesisBuilder":
                    eval_results = evaluator.build(data)
                    results["evaluation_results"]["hypotheses"] = eval_results

            except Exception as e:
                logger.error(f"Error in evaluator {evaluator.__class__.__name__}: {e}")
                results["evaluation_results"][evaluator.__class__.__name__.lower()] = {
                    "status": "error",
                    "error": str(e)
                }

        # Generate final recommendations
        self._generate_recommendations(results)

        results["status"] = "completed"
        return results

    def _generate_recommendations(self, results: Dict[str, Any]) -> None:
        """
        Generate final recommendations based on evaluation results.

        Args:
            results: Current results dictionary to update
        """
        recommendations = []

        # Check completeness
        completeness = results["evaluation_results"].get("completeness", {})
        if completeness.get("status") != "complete":
            recommendations.append({
                "type": "data_completion",
                "message": f"Data completeness: {completeness.get('completeness_score', 0):.2f}",
                "missing_fields": completeness.get("missing_fields", [])
            })

        # Check ambiguities
        ambiguities = results["evaluation_results"].get("ambiguities", {})
        if ambiguities.get("status") == "needs_review":
            recommendations.append({
                "type": "clarification_needed",
                "message": f"Found {ambiguities.get('ambiguities_found', 0)} ambiguities",
                "ambiguities": ambiguities.get("ambiguities", [])
            })

        # Check contradictions
        contradictions = results["evaluation_results"].get("contradictions", {})
        if contradictions.get("contradictions_found"):
            recommendations.append({
                "type": "logical_conflict",
                "message": f"Found {len(contradictions.get('contradictions', []))} logical contradictions",
                "contradictions": contradictions.get("contradictions", [])
            })

        # Check pipeline adjustments
        pipeline = results["evaluation_results"].get("pipeline", {})
        if pipeline.get("adjustments_needed"):
            recommendations.append({
                "type": "pipeline_adjustment",
                "message": "Pipeline adjustments recommended",
                "recommendations": pipeline.get("recommendations", [])
            })

        # Check queries
        queries = results["evaluation_results"].get("queries", {})
        if queries.get("queries_needed"):
            recommendations.append({
                "type": "user_clarification",
                "message": f"{len(queries.get('queries', []))} clarification queries generated",
                "queries": queries.get("queries", [])
            })

        # Check hypotheses
        hypotheses = results["evaluation_results"].get("hypotheses", {})
        if hypotheses.get("top_hypothesis"):
            recommendations.append({
                "type": "document_hypothesis",
                "message": f"Top hypothesis: {hypotheses['top_hypothesis']['type']} ({hypotheses['top_hypothesis']['confidence']:.2f})",
                "hypothesis": hypotheses.get("top_hypothesis")
            })

        results["final_recommendations"] = recommendations

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the ReasoningOrchestrator.

        Returns:
            Dictionary with status information
        """
        return {
            "agent": "ReasoningOrchestrator",
            "status": "ready",
            "evaluators_loaded": len(self.evaluators),
            "execution_order": self.execution_order
        }

# Import evaluators for type checking (circular import workaround)
# These imports are moved to the end to avoid circular dependencies
# In practice, the evaluators should be passed to the constructor


