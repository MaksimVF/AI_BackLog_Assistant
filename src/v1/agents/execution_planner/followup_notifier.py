





"""
Follow-up Notifier Agent
"""

from datetime import datetime, timedelta
from typing import Dict

class FollowUpNotifier:
    """
    Creates reminders and checkpoints based on task decision.
    """

    def create_reminders(self, decision: str, created_at: datetime, due_date: datetime) -> Dict:
        """
        Creates reminder schedule based on task decision.

        Args:
            decision: Decision (recommend, defer, reject)
            created_at: Task creation datetime
            due_date: Task due date

        Returns:
            Dictionary with reminder schedule
        """
        reminder_schedule = []
        checkpoints = []

        if decision == "recommend":
            # Mid-review reminder
            mid_review = created_at + (due_date - created_at) / 2
            reminder_schedule.append(mid_review.isoformat())

            # Checkpoint one day before deadline
            checkpoints.append((due_date - timedelta(days=1)).isoformat())

        elif decision == "defer":
            # Reminder after 3 days
            reminder_schedule.append((created_at + timedelta(days=3)).isoformat())

        # No reminders for rejected tasks

        return {
            "reminder_schedule": reminder_schedule,
            "checkpoints": checkpoints
        }






