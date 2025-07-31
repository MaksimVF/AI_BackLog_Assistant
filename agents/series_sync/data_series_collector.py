












"""
DataSeriesCollector for SeriesSync Agent

Collects and aggregates events based on time window and filters.
"""

from datetime import datetime
from typing import List, Dict, Optional

class DataSeriesCollector:
    """
    Collects and aggregates events from event logs based on time window and filters.
    """

    def __init__(self, event_log: List[Dict]):
        """
        Initialize with event log data.

        :param event_log: List of event dictionaries with 'timestamp' field
        """
        self.event_log = event_log

    def collect(
        self,
        time_window_start: str,
        time_window_end: str,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Collects events from event_log within time window and applying filters.

        :param time_window_start: Start date in 'YYYY-MM-DD' format
        :param time_window_end: End date in 'YYYY-MM-DD' format
        :param filters: Dictionary of filters (e.g., {'project': 'Alpha'})
        :return: List of filtered events
        """
        start_date = datetime.strptime(time_window_start, "%Y-%m-%d")
        end_date = datetime.strptime(time_window_end, "%Y-%m-%d")

        result = []
        for event in self.event_log:
            event_date = datetime.strptime(event.get("timestamp"), "%Y-%m-%d")
            if start_date <= event_date <= end_date:
                if self._passes_filters(event, filters):
                    result.append(event)

        return result

    def _passes_filters(self, event: Dict, filters: Optional[Dict]) -> bool:
        """
        Checks if event passes all filters.

        :param event: Event dictionary
        :param filters: Dictionary of filters
        :return: True if event passes all filters, False otherwise
        """
        if not filters:
            return True
        for key, value in filters.items():
            if event.get(key) != value:
                return False
        return True

