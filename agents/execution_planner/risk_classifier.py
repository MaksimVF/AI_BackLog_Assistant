





"""
Risk Classifier Agent
"""

import re
from typing import Dict, List

RISK_MARKERS = {
    "technical": ["нестабильный", "экспериментальный", "не протестирован", "отсутствие документации"],
    "external": ["внешняя команда", "третья сторона", "непредсказуемый", "регуляторный"],
    "resource": ["не хватает", "недостаточно", "ограниченный бюджет", "всего 1 человек"],
    "time": ["жесткий срок", "мало времени", "не укладываемся", "риск задержки"]
}

def classify_risks(task_description: str, constraints: Dict, stakeholders: List[str]) -> Dict:
    """
    Classifies risks based on task description and constraints.

    Args:
        task_description: Task description text
        constraints: Project constraints (deadline, budget, team_size)
        stakeholders: List of stakeholders

    Returns:
        Dictionary with risk assessment
    """
    risks = []
    text = task_description.lower()

    # Check for risk markers in description
    for category, markers in RISK_MARKERS.items():
        for marker in markers:
            if marker in text:
                risks.append({"category": category, "detail": marker})

    # Check team size constraint
    if constraints.get("team_size", 0) < 3:
        risks.append({"category": "resource", "detail": "маленькая команда"})

    # Check for external stakeholders
    if "external" in str(stakeholders):
        risks.append({"category": "external", "detail": "вовлечена внешняя сторона"})

    return {
        "has_risks": bool(risks),
        "risk_assessment": risks
    }







