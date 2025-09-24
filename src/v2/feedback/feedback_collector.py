




"""
Feedback Collector

Collects user feedback for:
- Classification decisions
- Prioritization choices
- Quality assessments
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class FeedbackCollector:
    """Collects and processes user feedback"""

    def __init__(self):
        """Initialize feedback collector"""
        self.feedback_store = []

    def collect_classification_feedback(self, document_id: str, user_category: str,
                                     original_category: str, confidence: float) -> Dict[str, Any]:
        """
        Collect feedback on document classification

        Args:
            document_id: ID of the document
            user_category: User-provided category
            original_category: Original classification category
            confidence: Original confidence score

        Returns:
            Feedback collection result
        """
        feedback = {
            "document_id": document_id,
            "type": "classification",
            "user_category": user_category,
            "original_category": original_category,
            "confidence": confidence,
            "timestamp": int(time.time())
        }

        self.feedback_store.append(feedback)
        logger.info(f"Collected classification feedback for {document_id}")

        return {
            "status": "collected",
            "feedback_id": len(self.feedback_store)
        }

    def collect_prioritization_feedback(self, document_id: str, user_priority: str,
                                      original_priority: str, priority_score: float) -> Dict[str, Any]:
        """
        Collect feedback on document prioritization

        Args:
            document_id: ID of the document
            user_priority: User-provided priority
            original_priority: Original priority level
            priority_score: Original priority score

        Returns:
            Feedback collection result
        """
        feedback = {
            "document_id": document_id,
            "type": "prioritization",
            "user_priority": user_priority,
            "original_priority": original_priority,
            "priority_score": priority_score,
            "timestamp": int(time.time())
        }

        self.feedback_store.append(feedback)
        logger.info(f"Collected prioritization feedback for {document_id}")

        return {
            "status": "collected",
            "feedback_id": len(self.feedback_store)
        }

    def collect_quality_feedback(self, document_id: str, user_score: float,
                              original_score: float, comments: str = "") -> Dict[str, Any]:
        """
        Collect feedback on document quality

        Args:
            document_id: ID of the document
            user_score: User-provided quality score
            original_score: Original quality score
            comments: User comments

        Returns:
            Feedback collection result
        """
        feedback = {
            "document_id": document_id,
            "type": "quality",
            "user_score": user_score,
            "original_score": original_score,
            "comments": comments,
            "timestamp": int(time.time())
        }

        self.feedback_store.append(feedback)
        logger.info(f"Collected quality feedback for {document_id}")

        return {
            "status": "collected",
            "feedback_id": len(self.feedback_store)
        }

    def get_feedback(self, document_id: str = None, feedback_type: str = None) -> List[Dict[str, Any]]:
        """
        Get collected feedback

        Args:
            document_id: Filter by document ID
            feedback_type: Filter by feedback type

        Returns:
            List of feedback items
        """
        filtered_feedback = self.feedback_store

        if document_id:
            filtered_feedback = [f for f in filtered_feedback if f["document_id"] == document_id]

        if feedback_type:
            filtered_feedback = [f for f in filtered_feedback if f["type"] == feedback_type]

        return filtered_feedback

    def process_feedback(self) -> Dict[str, Any]:
        """
        Process collected feedback

        Returns:
            Feedback processing summary
        """
        # Simple processing - can be enhanced
        summary = {
            "total_feedback": len(self.feedback_store),
            "by_type": {},
            "recent": []
        }

        # Process by type
        for feedback in self.feedback_store:
            feedback_type = feedback["type"]
            if feedback_type not in summary["by_type"]:
                summary["by_type"][feedback_type] = 0
            summary["by_type"][feedback_type] += 1

        # Get recent feedback
        summary["recent"] = self.feedback_store[-5:] if self.feedback_store else []

        logger.info(f"Processed {len(self.feedback_store)} feedback items")
        return summary




