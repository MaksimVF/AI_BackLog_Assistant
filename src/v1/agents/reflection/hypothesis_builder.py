





"""
HypothesisBuilder - Sub-agent for generating hypotheses about document content.

This agent analyzes extracted data and formulates hypotheses about the document's
nature, structure, and key information.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class HypothesisBuilder:
    def __init__(self):
        """
        Initialize the HypothesisBuilder.
        """
        self.hypothesis_rules = {
            "contract": {
                "keywords": ["договор", "соглашение", "стороны", "условия", "подписи",
                           "contract", "agreement", "parties", "terms", "signatures"],
                "structure": ["parties", "terms", "conditions", "signatures"],
                "confidence_threshold": 0.6
            },
            "financial_report": {
                "keywords": ["финансовый", "отчет", "доход", "расход", "прибыль",
                           "financial", "report", "revenue", "expense", "profit"],
                "structure": ["revenue", "expenses", "profit", "date_range"],
                "confidence_threshold": 0.7
            },
            "legal_document": {
                "keywords": ["закон", "регламент", "постановление", "статья",
                           "law", "regulation", "decree", "article"],
                "structure": ["title", "articles", "appendices", "references"],
                "confidence_threshold": 0.5
            }
        }

    def build(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate hypotheses about the document content.

        Args:
            data: Structured data to analyze

        Returns:
            Dictionary with hypotheses and confidence scores
        """
        hypotheses = []

        # Check each hypothesis type
        for doc_type, rules in self.hypothesis_rules.items():
            # Check keywords
            keyword_matches = sum(
                1 for keyword in rules["keywords"]
                if keyword.lower() in data.get("text", "").lower()
            )

            # Check structure
            structure_matches = sum(
                1 for section in rules["structure"]
                if section in data
            )

            # Calculate confidence
            confidence = min(1.0, (
                (keyword_matches / len(rules["keywords"])) * 0.6 +
                (structure_matches / len(rules["structure"])) * 0.4
            ))

            if confidence >= rules["confidence_threshold"]:
                hypotheses.append({
                    "type": doc_type,
                    "confidence": confidence,
                    "evidence": {
                        "keyword_matches": keyword_matches,
                        "structure_matches": structure_matches
                    }
                })

        # Sort by confidence
        hypotheses.sort(key=lambda x: x["confidence"], reverse=True)

        return {
            "hypotheses": hypotheses,
            "top_hypothesis": hypotheses[0] if hypotheses else None,
            "status": "clear" if hypotheses else "uncertain"
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the HypothesisBuilder.

        Returns:
            Dictionary with status information
        """
        return {
            "agent": "HypothesisBuilder",
            "status": "ready",
            "rules_loaded": len(self.hypothesis_rules),
            "supported_types": list(self.hypothesis_rules.keys())
        }





