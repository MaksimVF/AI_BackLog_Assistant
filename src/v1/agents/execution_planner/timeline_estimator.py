


"""
Timeline Estimator Agent
"""

from typing import Dict

def estimate_timeline(estimated_effort_days: int, priority: str, criticality: str) -> Dict:
    """
    Estimates task completion timeline based on effort, priority, and criticality.

    Args:
        estimated_effort_days: Estimated effort in days
        priority: Priority level (high, medium, low)
        criticality: Criticality level (high, medium, low)

    Returns:
        Dictionary with estimated duration
    """
    # Normalize input values
    priority = priority.lower()
    criticality = criticality.lower()

    if estimated_effort_days > 5:
        duration = round(estimated_effort_days * 1.5)
    elif priority == "high" and criticality == "high":
        duration = 1 if estimated_effort_days <= 1 else 2
    elif priority == "high":
        duration = 2 if estimated_effort_days <= 2 else 3
    elif priority == "medium":
        duration = 3 if estimated_effort_days <= 2 else 5
    else:
        duration = 5 if estimated_effort_days <= 3 else 7

    return {
        "estimated_duration_days": duration,
        "start_date": "to be set",
        "due_date": "to be calculated"
    }


