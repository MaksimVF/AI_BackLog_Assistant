




"""
ContradictionDetector - Sub-agent for identifying logical contradictions.

This agent analyzes structured data to find logical inconsistencies
and conflicting information.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ContradictionDetector:
    def __init__(self):
        """
        Initialize the ContradictionDetector.
        """
        # Define contradiction rules
        self.rules = [
            {
                "name": "date_conflict",
                "fields": ["start_date", "end_date"],
                "condition": lambda start, end: start and end and start > end,
                "message": "Дата начала позже даты окончания"
            },
            {
                "name": "tax_conflict",
                "fields": ["tax_info", "vat_amount"],
                "condition": lambda tax_info, vat: tax_info == "без НДС" and vat not in (None, 0),
                "message": "Указано 'без НДС', но присутствует сумма НДС"
            },
            {
                "name": "payment_conflict",
                "fields": ["payment_terms", "total_amount"],
                "condition": lambda terms, amount: "free" in terms.lower() and amount and amount > 0,
                "message": "Указано 'бесплатно', но присутствует сумма платежа"
            }
        ]

    def detect(self, structured_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Detect logical contradictions in the structured data.

        Args:
            structured_data: Data to analyze

        Returns:
            List of detected contradictions
        """
        contradictions = []

        for rule in self.rules:
            try:
                # Extract required fields
                field_values = []
                for field in rule["fields"]:
                    field_values.append(structured_data.get(field))

                # Check condition
                if rule["condition"](*field_values):
                    contradictions.append({
                        "type": rule["name"],
                        "fields": rule["fields"],
                        "issue": rule["message"],
                        "values": dict(zip(rule["fields"], field_values))
                    })
            except Exception as e:
                logger.warning(f"Error applying contradiction rule {rule['name']}: {e}")
                continue

        return contradictions

    def evaluate(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the data for contradictions and return results.

        Args:
            structured_data: Data to analyze

        Returns:
            Dictionary with contradiction evaluation results
        """
        contradictions = self.detect(structured_data)

        return {
            "contradictions_found": len(contradictions) > 0,
            "contradictions": contradictions,
            "recommendation": "Проверить логику документа" if contradictions else "OK",
            "status": "clear" if not contradictions else "conflict_detected"
        }

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the ContradictionDetector.

        Returns:
            Dictionary with status information
        """
        return {
            "agent": "ContradictionDetector",
            "status": "ready",
            "rules_loaded": len(self.rules),
            "supported_rules": [rule["name"] for rule in self.rules]
        }




