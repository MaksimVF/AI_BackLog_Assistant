


"""
CompletenessEvaluator - Sub-agent for assessing data completeness.

This agent evaluates whether all necessary information has been extracted
from the input sources.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CompletenessEvaluator:
    def __init__(self):
        """
        Initialize the CompletenessEvaluator.
        """
        self.rules = {
            "video": {
                "min_text_coverage": 0.6,
                "required_fields": ["transcript", "timestamps", "speaker_identification"]
            },
            "contract": {
                "required_sections": ["parties", "terms", "signatures", "appendices"],
                "min_section_coverage": 0.8
            },
            "financial_report": {
                "required_fields": ["revenue", "expenses", "profit", "date_range"],
                "min_field_coverage": 0.9
            }
        }

    def evaluate(self, data: Dict[str, Any], data_type: str = None) -> Dict[str, Any]:
        """
        Evaluate the completeness of the extracted data.

        Args:
            data: Structured data to evaluate
            data_type: Type of data (video, contract, financial_report, etc.)

        Returns:
            Dictionary with completeness evaluation results
        """
        result = {
            "completeness_score": 1.0,
            "missing_fields": [],
            "coverage": 1.0,
            "status": "complete"
        }

        if not data_type or data_type not in self.rules:
            logger.warning(f"No completeness rules for data type: {data_type}")
            return result

        # Check required fields
        missing_fields = []
        if "required_fields" in self.rules[data_type]:
            for field in self.rules[data_type]["required_fields"]:
                if field not in data or not data[field]:
                    missing_fields.append(field)

        # Calculate completeness score
        if missing_fields:
            result["completeness_score"] = max(0.0, 1.0 - (len(missing_fields) / len(self.rules[data_type]["required_fields"])))
            result["status"] = "incomplete"

        # Check coverage thresholds
        if "min_text_coverage" in self.rules[data_type]:
            text_coverage = data.get("text_coverage", 1.0)
            if text_coverage < self.rules[data_type]["min_text_coverage"]:
                result["coverage"] = text_coverage
                result["status"] = "partial"

        result["missing_fields"] = missing_fields
        return result

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the CompletenessEvaluator.

        Returns:
            Dictionary with status information
        """
        return {
            "agent": "CompletenessEvaluator",
            "status": "ready",
            "rules_loaded": len(self.rules),
            "supported_types": list(self.rules.keys())
        }


