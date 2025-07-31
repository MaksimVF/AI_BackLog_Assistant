






"""
Dependency Detector Agent
"""

import re
from typing import Dict, List

DEPENDENCY_MARKERS = [
    "необходимо дождаться", "после завершения", "зависит от",
    "требуется", "нужно получить", "блокируется"
]

def detect_dependencies(task_description: str, linked_tasks: List[str], stakeholders: List[str]) -> Dict:
    """
    Detects dependencies in task description and metadata.

    Args:
        task_description: Task description text
        linked_tasks: List of linked task IDs
        stakeholders: List of stakeholders

    Returns:
        Dictionary with dependency information
    """
    dependencies = []

    # Check for dependency markers in description
    text = task_description.lower()
    for marker in DEPENDENCY_MARKERS:
        if marker in text:
            dependencies.append({"type": "textual", "description": marker})

    # Add linked tasks as dependencies
    for task in linked_tasks:
        dependencies.append({"type": "task_link", "reference": task})

    # Add stakeholders as dependencies
    for person in stakeholders:
        dependencies.append({"type": "stakeholder", "name": person})

    return {
        "has_dependencies": bool(dependencies),
        "dependency_details": dependencies
    }







