











"""
Mock Storage for Testing

In-memory storage implementation for testing service agents.
"""

from typing import Any, Dict, List

class InMemoryStorage:
    """
    In-memory storage for testing service agents.
    """

    def __init__(self):
        """Initialize in-memory storage"""
        self.audit_logs: List[Dict[str, Any]] = []
        self.feedback_logs: List[Dict[str, Any]] = []

    def save_audit(self, record: Dict[str, Any]):
        """Save audit record"""
        self.audit_logs.append(record)

    def save_feedback(self, record: Dict[str, Any]):
        """Save feedback record"""
        self.feedback_logs.append(record)












