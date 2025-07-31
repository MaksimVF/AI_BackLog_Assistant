








"""
Response Formatter Agent

Collects and formats final response from analysis agents.
"""

from datetime import datetime
from typing import Any, Dict, Optional

class ResponseFormatter:
    """
    Collects and formats final response from analysis agents.
    """

    def __init__(self):
        pass

    def format(
        self,
        task_id: str,
        decision_result: Dict[str, Any],
        priority_data: Dict[str, Any],
        effort_data: Dict[str, Any],
        deadline: str,
        visuals: Optional[Dict[str, Any]] = None,
        schedule: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Formats final response from analysis results.

        Args:
            task_id: Task identifier
            decision_result: Decision result data
            priority_data: Priority analysis data
            effort_data: Effort estimation data
            deadline: Calculated deadline
            visuals: Visualization data
            schedule: Scheduling data

        Returns:
            Formatted response
        """
        return {
            "task_id": task_id,
            "status": decision_result.get("status", "unknown"),
            "summary": decision_result.get("explanation", "No explanation available"),
            "priority_score": priority_data.get("priority_score", 0),
            "effort_estimate": effort_data.get("effort_estimate", "Unknown"),
            "deadline": deadline,
            "visuals": visuals or {},
            "schedule": schedule or {},
            "meta": {
                "created_by": "AI-Agent-v1.0",
                "generated_at": datetime.utcnow().isoformat(),
                "confidence_level": decision_result.get("confidence", "medium")
            }
        }









