



"""
Historical Performance Agent
"""

from typing import Dict, List
from .models import TaskData

class HistoricalPerformanceAgent:
    """
    Analyzes historical data about similar task execution.
    Helps predict execution time and potential issues.
    """

    def __init__(self):
        # In a real implementation, this would connect to a database
        self.historical_data = {
            "similar_tasks": [
                {"type": "bug", "avg_time": 4, "success_rate": 0.9},
                {"type": "feature", "avg_time": 8, "success_rate": 0.8},
                {"type": "refactoring", "avg_time": 6, "success_rate": 0.85}
            ]
        }

    def analyze_performance(self, task_data: TaskData) -> Dict:
        """
        Analyzes historical performance for similar tasks.

        Args:
            task_data: Task data

        Returns:
            Historical performance analysis
        """
        task_type = task_data.get("type", "").lower()
        estimated_time = task_data.get("estimated_time_hours", 0)

        # Find similar tasks
        similar = None
        for item in self.historical_data["similar_tasks"]:
            if item["type"] == task_type:
                similar = item
                break

        if similar:
            time_diff = abs(estimated_time - similar["avg_time"])
            time_ratio = estimated_time / similar["avg_time"] if similar["avg_time"] > 0 else 1

            # Determine time realism
            if time_ratio > 1.5:
                time_label = "overestimated"
            elif time_ratio < 0.7:
                time_label = "underestimated"
            else:
                time_label = "realistic"

            return {
                "historical_avg_time": similar["avg_time"],
                "historical_success_rate": similar["success_rate"],
                "time_estimation": time_label,
                "time_difference": time_diff
            }
        else:
            return {
                "historical_avg_time": None,
                "historical_success_rate": None,
                "time_estimation": "unknown",
                "time_difference": None
            }




