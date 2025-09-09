



"""
Dependency Agent
"""

from typing import Dict, List
from .models import TaskData

class DependencyAgent:
    """
    Analyzes dependencies between tasks and projects.
    Considers blocking tasks and interrelationships for proper ranking.
    """

    def __init__(self):
        pass

    def analyze_dependencies(self, task_data: TaskData) -> Dict:
        """
        Analyzes dependencies for a given task.

        Args:
            task_data: Task data

        Returns:
            Dependency analysis results
        """
        dependencies = task_data.get("dependencies", [])
        blocked_by = task_data.get("blocked_by", [])
        blocks = task_data.get("blocks", [])
        external_deps = task_data.get("external_dependencies", [])

        dependency_issues = []

        # Check for dependencies
        if dependencies:
            dependency_issues.append(f"Depends on {len(dependencies)} task(s)")

        # Check for blocking tasks
        if blocked_by:
            dependency_issues.append(f"Blocked by {len(blocked_by)} task(s)")

        # Check for tasks this blocks
        if blocks:
            dependency_issues.append(f"Blocks {len(blocks)} task(s)")

        # Check for external dependencies
        if external_deps:
            dependency_issues.append(f"Has {len(external_deps)} external dependency(ies)")

        # Determine dependency severity
        total_deps = len(dependencies) + len(blocked_by) + len(external_deps)
        if total_deps > 3:
            severity = "high"
        elif total_deps > 0:
            severity = "medium"
        else:
            severity = "low"

        return {
            "dependency_severity": severity,
            "dependency_issues": dependency_issues,
            "total_dependencies": total_deps
        }



