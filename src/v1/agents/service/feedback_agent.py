










"""
Feedback Agent

Collects and stores user feedback on results.
"""

from datetime import datetime
from typing import Any, Dict, Optional

class FeedbackAgent:
    """
    Collects and stores user feedback on results.
    """

    def __init__(self, storage_backend: Any):
        """
        Initialize FeedbackAgent with storage backend.

        Args:
            storage_backend: Storage backend
        """
        self.storage = storage_backend

    def run(
        self,
        task_id: str,
        user_rating: str,
        user_comment: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Records user feedback.

        Args:
            task_id: Task identifier
            user_rating: User rating ('positive', 'negative', 'neutral')
            user_comment: User comment (optional)
            user_id: User identifier (optional)

        Returns:
            Feedback record
        """
        feedback_record = {
            "task_id": task_id,
            "user_id": user_id,
            "rating": user_rating,
            "comment": user_comment,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._save(feedback_record)
        return feedback_record

    def _save(self, record: Dict[str, Any]):
        """Saves feedback record to storage"""
        self.storage.save_feedback(record)











