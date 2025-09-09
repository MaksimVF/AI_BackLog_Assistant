



"""
AmbiguityResolver - Sub-agent for identifying and resolving ambiguities.

This agent detects unclear fragments, logical contradictions, or context gaps
in the extracted data.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AmbiguityResolver:
    def __init__(self):
        """
        Initialize the AmbiguityResolver.
        """
        self.patterns = {
            "pronoun_ambiguity": r"\b(?:он|она|оно|они|it|they|he|she)\b",
            "vague_reference": r"\b(?:этот|тот|this|that|the|a)\b\s+\w+",
            "incomplete_date": r"\b\d{2}\.\d{2}\b",  # Dates without year
            "missing_context": r"\b(?:согласно|в соответствии|according to|per)\b"
        }

    def resolve(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify and resolve ambiguities in the data.

        Args:
            data: Structured data to analyze

        Returns:
            Dictionary with ambiguity resolution results
        """
        ambiguities = []

        # Check for pronoun ambiguities
        if "text" in data:
            text = data["text"]
            for pattern_name, pattern in self.patterns.items():
                # Simple pattern matching (would be replaced with NLP in production)
                if pattern_name in text.lower():
                    ambiguities.append({
                        "type": pattern_name,
                        "text": text,
                        "suggestion": f"Review {pattern_name} in: {text[:50]}..."
                    })

        return {
            "ambiguities_found": len(ambiguities),
            "ambiguities": ambiguities,
            "status": "clear" if not ambiguities else "needs_review"
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the AmbiguityResolver.

        Returns:
            Dictionary with status information
        """
        return {
            "agent": "AmbiguityResolver",
            "status": "ready",
            "patterns_loaded": len(self.patterns),
            "supported_patterns": list(self.patterns.keys())
        }



