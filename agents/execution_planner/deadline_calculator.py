



"""
Deadline Calculator Agent
"""

from datetime import datetime, timedelta
from typing import Dict

class DeadlineCalculator:
    """
    Calculates task deadline based on effort and working hours.
    """

    def __init__(self, working_hours_per_day: int = 6):
        self.working_hours_per_day = working_hours_per_day

    def calculate_deadline(self, current_dt: datetime, effort_hours: int) -> datetime:
        """
        Calculates deadline considering working days only.

        Args:
            current_dt: Current date and time
            effort_hours: Estimated effort in hours

        Returns:
            Calculated deadline datetime
        """
        days_needed = (effort_hours + self.working_hours_per_day - 1) // self.working_hours_per_day
        deadline = current_dt

        while days_needed > 0:
            deadline += timedelta(days=1)
            if deadline.weekday() < 5:  # Monday=0, Friday=4 - working days
                days_needed -= 1

        # Set end of workday time
        deadline = deadline.replace(hour=18, minute=0, second=0, microsecond=0)
        return deadline

    def calculate_deadline_info(self, current_dt: datetime, effort_hours: int) -> Dict:
        """
        Calculates deadline and returns structured information.

        Args:
            current_dt: Current date and time
            effort_hours: Estimated effort in hours

        Returns:
            Dictionary with deadline information
        """
        deadline = self.calculate_deadline(current_dt, effort_hours)
        effort_days_required = (effort_hours + self.working_hours_per_day - 1) // self.working_hours_per_day

        return {
            "deadline_date": deadline.isoformat(),
            "effort_days_required": effort_days_required
        }



