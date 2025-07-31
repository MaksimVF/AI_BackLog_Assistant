



"""
User Feedback Agent
"""

from typing import Dict, List
from .models import TaskData

class UserFeedbackAgent:
    """
    Integrates user feedback data for task prioritization.
    Considers feedback from users or stakeholders to adjust task importance.
    """

    def __init__(self):
        self.feedback_weights = {
            "positive": 0.8,
            "neutral": 0.5,
            "negative": 0.2
        }

    def analyze_feedback(self, task_data: TaskData) -> Dict:
        """
        Analyzes user feedback for a given task.

        Args:
            task_data: Task data

        Returns:
            User feedback analysis results
        """
        feedback = task_data.get("user_feedback", [])
        feedback_score = 0.0
        feedback_summary = []

        # Analyze feedback
        if feedback:
            for fb in feedback:
                sentiment = fb.get("sentiment", "neutral")
                comment = fb.get("comment", "")

                feedback_score += self.feedback_weights.get(sentiment, 0.5)
                feedback_summary.append(f"{sentiment.capitalize()}: {comment}")

            # Average the feedback score
            feedback_score /= len(feedback)

        # Determine feedback label
        if feedback_score > 0.7:
            label = "positive"
        elif feedback_score > 0.4:
            label = "neutral"
        else:
            label = "negative"

        return {
            "feedback_score": round(feedback_score, 2),
            "feedback_label": label,
            "feedback_summary": feedback_summary
        }




