





"""
Feedback Processing System

Handles user feedback for:
- Model retraining
- Adaptive learning
- Continuous improvement
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class FeedbackProcessor:
    """Processes user feedback for model improvement"""

    def __init__(self):
        """Initialize feedback processor"""
        self.feedback_queue = []

    def collect_feedback(self, document_id: str, feedback_type: str,
                       feedback_data: Dict[str, Any]):
        """
        Collect user feedback

        Args:
            document_id: ID of the document
            feedback_type: Type of feedback (classification, prioritization, quality)
            feedback_data: Feedback data
        """
        try:
            feedback_item = {
                "document_id": document_id,
                "type": feedback_type,
                "data": feedback_data,
                "timestamp": int(time.time())
            }

            self.feedback_queue.append(feedback_item)
            logger.info(f"Collected feedback for {document_id}: {feedback_type}")

        except Exception as e:
            logger.error(f"Feedback collection failed: {e}")
            raise

    def process_feedback(self) -> Dict[str, Any]:
        """
        Process collected feedback

        Returns:
            Summary of processed feedback
        """
        try:
            if not self.feedback_queue:
                return {"status": "no_feedback"}

            # Group feedback by type
            feedback_summary = {
                "classification": [],
                "prioritization": [],
                "quality": []
            }

            for item in self.feedback_queue:
                feedback_type = item["type"]
                if feedback_type in feedback_summary:
                    feedback_summary[feedback_type].append(item["data"])

            # Clear queue
            processed_count = len(self.feedback_queue)
            self.feedback_queue = []

            logger.info(f"Processed {processed_count} feedback items")
            return {
                "status": "processed",
                "count": processed_count,
                "summary": feedback_summary
            }

        except Exception as e:
            logger.error(f"Feedback processing failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def apply_feedback_to_models(self, classifier_model, prioritization_model, quality_model):
        """
        Apply feedback to update models

        Args:
            classifier_model: Document classifier model
            prioritization_model: Prioritization model
            quality_model: Quality analysis model
        """
        try:
            # Process feedback first
            summary = self.process_feedback()

            # Update classifier model
            for feedback in summary.get("summary", {}).get("classification", []):
                document = feedback.get("document", "")
                correct_label = feedback.get("correct_label", "")
                if document and correct_label:
                    classifier_model.update_with_feedback(document, correct_label)

            # Update prioritization model
            for feedback in summary.get("summary", {}).get("prioritization", []):
                document_data = feedback.get("document_data", {})
                correct_priority = feedback.get("correct_priority", "")
                if document_data and correct_priority:
                    prioritization_model.update_with_feedback(document_data, correct_priority)

            logger.info("Applied feedback to all models")

        except Exception as e:
            logger.error(f"Model feedback application failed: {e}")
            raise





