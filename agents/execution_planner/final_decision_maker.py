







"""
Final Decision Maker Agent
"""

from typing import Dict

def make_final_decision(input_data: Dict) -> Dict:
    """
    Makes final decision based on task analysis.

    Args:
        input_data: Task analysis data including priority, consistency, effort, etc.

    Returns:
        Dictionary with final decision and reason
    """
    score = input_data.get("priority_score", 0)
    consistency = input_data.get("consistency_check", {}).get("is_consistent", False)
    effort = input_data.get("effort_estimate", "medium")
    criticality = input_data.get("criticality", "medium")
    aligned = input_data.get("strategic_alignment", False)

    if not consistency or not aligned:
        return {
            "decision": "reject",
            "reason": "Несогласованность или отсутствие стратегической значимости"
        }

    if score >= 7 and effort in ["low", "medium"]:
        return {
            "decision": "approve",
            "reason": "Высокий приоритет при приемлемых затратах"
        }

    if score >= 5 and effort == "high" and criticality != "high":
        return {
            "decision": "defer",
            "reason": "Высокие усилия при среднем приоритете и некритичной задаче"
        }

    return {
        "decision": "reject",
        "reason": "Низкий приоритет или чрезмерные усилия"
    }








