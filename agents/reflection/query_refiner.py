




"""
QueryRefiner - Sub-agent for formulating clarification queries.

This agent generates questions to address information gaps or ambiguities.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class QueryRefiner:
    def __init__(self):
        """
        Initialize the QueryRefiner.
        """
        self.query_templates = {
            "missing_field": "Please provide the {field_name} from the document.",
            "low_confidence": "Can you confirm the accuracy of: {text}?",
            "ambiguous_reference": "Who or what does '{reference}' refer to in: {context}?",
            "incomplete_date": "What is the full date for: {partial_date}?",
            "missing_signature": "Is the document signed? If yes, please provide the signature page."
        }

    def refine(self, data: Dict[str, Any], evaluation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate clarification queries based on evaluation results.

        Args:
            data: Structured data
            evaluation_results: Results from other evaluators

        Returns:
            Dictionary with refined queries
        """
        queries = []

        # Generate queries for missing fields
        completeness_results = evaluation_results.get("completeness", {})
        for field in completeness_results.get("missing_fields", []):
            queries.append(self.query_templates["missing_field"].format(field_name=field))

        # Generate queries for ambiguities
        ambiguity_results = evaluation_results.get("ambiguities", {})
        for ambiguity in ambiguity_results.get("ambiguities", []):
            if isinstance(ambiguity, dict):
                if ambiguity.get("type") == "pronoun_ambiguity":
                    text = ambiguity.get("text", "")
                    queries.append(self.query_templates["ambiguous_reference"].format(
                        reference=text.split()[0] if text else "",
                        context=text
                    ))
                elif ambiguity.get("type") == "incomplete_date":
                    queries.append(self.query_templates["incomplete_date"].format(
                        partial_date=ambiguity.get("text", "")
                    ))

        # Check for low confidence scores
        completeness_score = completeness_results.get("completeness_score", 1.0)
        if completeness_score < 0.7:
            queries.append(self.query_templates["low_confidence"].format(
                text=data.get("summary", "the extracted information")
            ))

        return {
            "queries": queries,
            "queries_needed": len(queries) > 0,
            "status": "clear" if not queries else "needs_clarification"
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the QueryRefiner.

        Returns:
            Dictionary with status information
        """
        return {
            "agent": "QueryRefiner",
            "status": "ready",
            "templates_loaded": len(self.query_templates)
        }




