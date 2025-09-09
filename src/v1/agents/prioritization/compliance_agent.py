




"""
Compliance Agent
"""

from typing import Dict, List
from .models import TaskData

class ComplianceAgent:
    """
    Checks task compliance with regulatory requirements, company policies, or industry standards.
    Important for financial, legal, and critical IT projects.
    """

    def __init__(self):
        # Example compliance rules
        self.compliance_rules = {
            "security": ["auth", "encryption", "vulnerability", "access control"],
            "privacy": ["gdpr", "personal data", "user consent", "data protection"],
            "financial": ["audit", "reporting", "compliance", "regulation"],
            "quality": ["testing", "code review", "documentation", "standards"]
        }

    def check_compliance(self, task_data: TaskData) -> Dict:
        """
        Checks compliance for a given task.

        Args:
            task_data: Task data

        Returns:
            Compliance check results
        """
        title = task_data.get("title", "").lower()
        description = task_data.get("description", "").lower()
        task_type = task_data.get("type", "").lower()

        compliance_issues = []
        compliance_score = 0.0

        # Check each compliance area
        for area, keywords in self.compliance_rules.items():
            # Check if task mentions compliance-related terms
            if any(keyword in title or keyword in description for keyword in keywords):
                compliance_score += 0.2
                compliance_issues.append(f"Requires {area} compliance")

        # Check for specific compliance requirements
        if "compliance" in task_type or "regulation" in task_type:
            compliance_score += 0.3
            compliance_issues.append("Explicitly marked as compliance task")

        # Determine compliance level
        if compliance_score > 0.6:
            level = "high"
        elif compliance_score > 0.3:
            level = "medium"
        else:
            level = "low"

        return {
            "compliance_level": level,
            "compliance_score": round(compliance_score, 2),
            "compliance_issues": compliance_issues
        }





