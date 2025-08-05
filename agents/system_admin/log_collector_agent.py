

import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent

# Try to import ClickHouse client
try:
    from database.clickhouse_client import ClickHouseClient
    from config.clickhouse_config import get_clickhouse_config
    HAS_CLICKHOUSE = True
except ImportError:
    HAS_CLICKHOUSE = False
    ClickHouseClient = None

class LogCollectorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="LogCollectorAgent")
        self.collected_logs: List[Dict] = []
        self.logger = logging.getLogger("LogCollectorAgent")

        # Initialize ClickHouse client
        self.clickhouse_client = None
        if HAS_CLICKHOUSE:
            try:
                config = get_clickhouse_config()
                self.clickhouse_client = ClickHouseClient(config)
                if not self.clickhouse_client.is_connected():
                    self.logger.warning("ClickHouse client not connected, using in-memory logs only")
                    self.clickhouse_client = None
            except Exception as e:
                self.logger.error(f"Failed to initialize ClickHouse client: {e}")
                self.clickhouse_client = None

    def collect_log(self, source: str, level: str, message: str, context: Dict = None):
        """Collect a log from a given source"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "level": level.upper(),
            "message": message,
            "context": context or {}
        }
        self.collected_logs.append(log_entry)
        self.logger.debug(f"Log collected: {log_entry}")

        # Also store in ClickHouse if available
        if self.clickhouse_client:
            try:
                self.clickhouse_client.store_log(
                    level=level.upper(),
                    source=source,
                    message=message,
                    metadata=context or {},
                    agent_id=self.name
                )
            except Exception as e:
                self.logger.error(f"Failed to store log in ClickHouse: {e}")

    def filter_logs(self, level: str = "ERROR") -> List[Dict]:
        """Filter logs by level"""
        return [log for log in self.collected_logs if log["level"] == level.upper()]

    def export_logs(self) -> List[Dict]:
        """Return all collected logs"""
        return self.collected_logs

    def clear_logs(self):
        """Clear all logs (e.g., at the end of a monitoring session)"""
        self.logger.debug("Logs cleared.")
        self.collected_logs.clear()

    def query_logs(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        level: Optional[str] = None,
        source: Optional[str] = None,
        limit: Optional[int] = 1000
    ) -> List[Dict]:
        """
        Query logs from ClickHouse (if available) or fallback to in-memory logs

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            level: Log level to filter by
            source: Source to filter by
            limit: Maximum number of results to return

        Returns:
            List of log entries
        """
        if self.clickhouse_client:
            try:
                return self.clickhouse_client.query_logs(
                    time_range=time_range,
                    level=level,
                    source=source,
                    limit=limit
                )
            except Exception as e:
                self.logger.error(f"Failed to query logs from ClickHouse: {e}")
                # Fallback to in-memory logs
                return self._filter_in_memory_logs(time_range, level, source, limit)
        else:
            return self._filter_in_memory_logs(time_range, level, source, limit)

    def _filter_in_memory_logs(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        level: Optional[str] = None,
        source: Optional[str] = None,
        limit: Optional[int] = 1000
    ) -> List[Dict]:
        """Filter in-memory logs based on criteria"""
        filtered_logs = self.collected_logs

        if time_range:
            if time_range.get('start'):
                filtered_logs = [
                    log for log in filtered_logs
                    if datetime.fromisoformat(log['timestamp']) >= time_range['start']
                ]
            if time_range.get('end'):
                filtered_logs = [
                    log for log in filtered_logs
                    if datetime.fromisoformat(log['timestamp']) <= time_range['end']
                ]

        if level:
            filtered_logs = [log for log in filtered_logs if log['level'] == level.upper()]

        if source:
            filtered_logs = [log for log in filtered_logs if log['source'] == source]

        if limit:
            filtered_logs = filtered_logs[-limit:]  # Get most recent logs

        return filtered_logs

    def get_log_stats(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        level: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get log statistics from ClickHouse (if available) or in-memory logs

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            level: Log level to filter by

        Returns:
            Dictionary with log statistics
        """
        if self.clickhouse_client:
            try:
                return self.clickhouse_client.get_log_stats(time_range=time_range, level=level)
            except Exception as e:
                self.logger.error(f"Failed to get log stats from ClickHouse: {e}")
                # Fallback to in-memory stats
                return self._get_in_memory_log_stats(time_range, level)
        else:
            return self._get_in_memory_log_stats(time_range, level)

    def _get_in_memory_log_stats(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        level: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get statistics from in-memory logs"""
        filtered_logs = self._filter_in_memory_logs(time_range, level)

        # Count by level
        level_counts = {}
        for log in filtered_logs:
            log_level = log['level']
            level_counts[log_level] = level_counts.get(log_level, 0) + 1

        return {
            'total': len(filtered_logs),
            'by_level': level_counts
        }

