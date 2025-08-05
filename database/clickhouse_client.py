

"""
ClickHouse client for logs and metrics storage
"""

import os
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

try:
    from clickhouse_connect import Client, ClientException
except ImportError:
    Client = None
    ClientException = Exception

logger = logging.getLogger(__name__)

class ClickHouseClient:
    """ClickHouse client for storing and querying logs and metrics"""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize ClickHouse client

        Args:
            config: Configuration dictionary with ClickHouse connection parameters
        """
        self.config = config or {}
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize ClickHouse client from configuration"""
        if Client is None:
            logger.warning("clickhouse-connect not installed, using mock client")
            return

        # Load configuration from environment variables if not provided
        config = {
            'host': self.config.get('host') or os.getenv('CLICKHOUSE_HOST', 'localhost'),
            'port': self.config.get('port') or os.getenv('CLICKHOUSE_PORT', 8443),
            'username': self.config.get('username') or os.getenv('CLICKHOUSE_USER', 'default'),
            'password': self.config.get('password') or os.getenv('CLICKHOUSE_PASSWORD', ''),
            'database': self.config.get('database') or os.getenv('CLICKHOUSE_DATABASE', 'ai_backlog_admin'),
            'secure': self.config.get('secure', True),
            'verify': self.config.get('verify', True),
            'ca_cert': self.config.get('ca_cert') or os.getenv('CLICKHOUSE_CA_CERT'),
        }

        try:
            self.client = Client(**config)
            self._test_connection()
        except Exception as e:
            logger.error(f"Failed to initialize ClickHouse client: {e}")
            self.client = None

    def _test_connection(self):
        """Test ClickHouse connection"""
        if not self.client:
            return False

        try:
            result = self.client.command('SELECT 1')
            return result == '1\n'
        except Exception as e:
            logger.error(f"ClickHouse connection test failed: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self.client is not None

    def store_log(
        self,
        level: str,
        source: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[Union[str, UUID]] = None
    ) -> bool:
        """
        Store a log entry in ClickHouse

        Args:
            level: Log level (info, warning, error, etc.)
            source: Source of the log
            message: Log message
            metadata: Additional metadata as dictionary
            agent_id: ID of the agent generating the log
            session_id: Session ID

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            if session_id and not isinstance(session_id, UUID):
                try:
                    session_id = UUID(session_id)
                except ValueError:
                    session_id = uuid4()

            if not session_id:
                session_id = uuid4()

            if metadata is None:
                metadata = {}

            # Convert metadata to JSON string for Map type
            metadata_str = json.dumps(metadata)

            query = """
            INSERT INTO logs (
                timestamp, level, source, message, metadata, agent_id, session_id
            ) VALUES
            """
            values = [
                (datetime.utcnow(), level, source, message, metadata_str, agent_id, session_id)
            ]

            self.client.insert('logs', values, column_names=[
                'timestamp', 'level', 'source', 'message', 'metadata', 'agent_id', 'session_id'
            ])

            return True
        except Exception as e:
            logger.error(f"Failed to store log: {e}")
            return False

    def store_metric(
        self,
        metric_name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[Union[str, UUID]] = None
    ) -> bool:
        """
        Store a metric in ClickHouse

        Args:
            metric_name: Name of the metric
            value: Metric value
            tags: Additional tags as dictionary
            agent_id: ID of the agent generating the metric
            session_id: Session ID

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            if session_id and not isinstance(session_id, UUID):
                try:
                    session_id = UUID(session_id)
                except ValueError:
                    session_id = uuid4()

            if not session_id:
                session_id = uuid4()

            if tags is None:
                tags = {}

            # Convert tags to JSON string for Map type
            tags_str = json.dumps(tags)

            query = """
            INSERT INTO metrics (
                timestamp, metric_name, value, tags, agent_id, session_id
            ) VALUES
            """
            values = [
                (datetime.utcnow(), metric_name, value, tags_str, agent_id, session_id)
            ]

            self.client.insert('metrics', values, column_names=[
                'timestamp', 'metric_name', 'value', 'tags', 'agent_id', 'session_id'
            ])

            return True
        except Exception as e:
            logger.error(f"Failed to store metric: {e}")
            return False

    def store_event(
        self,
        event_type: str,
        source: str,
        details: str,
        metadata: Optional[Dict[str, Any]] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[Union[str, UUID]] = None
    ) -> bool:
        """
        Store an event in ClickHouse

        Args:
            event_type: Type of event
            source: Source of the event
            details: Event details
            metadata: Additional metadata as dictionary
            agent_id: ID of the agent generating the event
            session_id: Session ID

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            return False

        try:
            if session_id and not isinstance(session_id, UUID):
                try:
                    session_id = UUID(session_id)
                except ValueError:
                    session_id = uuid4()

            if not session_id:
                session_id = uuid4()

            if metadata is None:
                metadata = {}

            # Convert metadata to JSON string for Map type
            metadata_str = json.dumps(metadata)

            query = """
            INSERT INTO events (
                timestamp, event_type, source, details, metadata, agent_id, session_id
            ) VALUES
            """
            values = [
                (datetime.utcnow(), event_type, source, details, metadata_str, agent_id, session_id)
            ]

            self.client.insert('events', values, column_names=[
                'timestamp', 'event_type', 'source', 'details', 'metadata', 'agent_id', 'session_id'
            ])

            return True
        except Exception as e:
            logger.error(f"Failed to store event: {e}")
            return False

    def query_logs(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        level: Optional[str] = None,
        source: Optional[str] = None,
        limit: Optional[int] = 1000
    ) -> List[Dict[str, Any]]:
        """
        Query logs from ClickHouse

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            level: Log level to filter by
            source: Source to filter by
            limit: Maximum number of results to return

        Returns:
            List of log entries as dictionaries
        """
        if not self.client:
            return []

        try:
            query = "SELECT * FROM logs WHERE 1=1"
            params = []

            if time_range:
                if time_range.get('start'):
                    query += " AND timestamp >= %s"
                    params.append(time_range['start'])
                if time_range.get('end'):
                    query += " AND timestamp <= %s"
                    params.append(time_range['end'])

            if level:
                query += " AND level = %s"
                params.append(level)

            if source:
                query += " AND source = %s"
                params.append(source)

            query += " ORDER BY timestamp DESC"

            if limit:
                query += " LIMIT %s"
                params.append(limit)

            result = self.client.query(query, params=params)
            return [dict(row) for row in result.result_rows]
        except Exception as e:
            logger.error(f"Failed to query logs: {e}")
            return []

    def query_metrics(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        metric_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        limit: Optional[int] = 1000
    ) -> List[Dict[str, Any]]:
        """
        Query metrics from ClickHouse

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            metric_name: Metric name to filter by
            tags: Tags to filter by
            limit: Maximum number of results to return

        Returns:
            List of metric entries as dictionaries
        """
        if not self.client:
            return []

        try:
            query = "SELECT * FROM metrics WHERE 1=1"
            params = []

            if time_range:
                if time_range.get('start'):
                    query += " AND timestamp >= %s"
                    params.append(time_range['start'])
                if time_range.get('end'):
                    query += " AND timestamp <= %s"
                    params.append(time_range['end'])

            if metric_name:
                query += " AND metric_name = %s"
                params.append(metric_name)

            if tags:
                for key, value in tags.items():
                    query += f" AND has(tags, '{key}') AND tags['{key}'] = '{value}'"

            query += " ORDER BY timestamp DESC"

            if limit:
                query += " LIMIT %s"
                params.append(limit)

            result = self.client.query(query, params=params)
            return [dict(row) for row in result.result_rows]
        except Exception as e:
            logger.error(f"Failed to query metrics: {e}")
            return []

    def get_log_stats(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        level: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get log statistics

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            level: Log level to filter by

        Returns:
            Dictionary with log statistics
        """
        if not self.client:
            return {}

        try:
            query = "SELECT count() as total FROM logs WHERE 1=1"
            params = []

            if time_range:
                if time_range.get('start'):
                    query += " AND timestamp >= %s"
                    params.append(time_range['start'])
                if time_range.get('end'):
                    query += " AND timestamp <= %s"
                    params.append(time_range['end'])

            if level:
                query += " AND level = %s"
                params.append(level)

            result = self.client.query(query, params=params)
            total = result.result_rows[0][0] if result.result_rows else 0

            # Get count by level
            level_query = """
            SELECT level, count() as count
            FROM logs
            WHERE 1=1
            """
            level_params = []

            if time_range:
                if time_range.get('start'):
                    level_query += " AND timestamp >= %s"
                    level_params.append(time_range['start'])
                if time_range.get('end'):
                    level_query += " AND timestamp <= %s"
                    level_params.append(time_range['end'])

            if level:
                level_query += " AND level = %s"
                level_params.append(level)

            level_query += " GROUP BY level"

            level_result = self.client.query(level_query, params=level_params)
            level_counts = {row[0]: row[1] for row in level_result.result_rows}

            return {
                'total': total,
                'by_level': level_counts
            }
        except Exception as e:
            logger.error(f"Failed to get log stats: {e}")
            return {}

    def get_metric_aggregations(
        self,
        time_range: Optional[Dict[str, datetime]] = None,
        metric_name: Optional[str] = None,
        aggregation: str = 'hour'
    ) -> Dict[str, Any]:
        """
        Get metric aggregations

        Args:
            time_range: Dictionary with 'start' and 'end' datetime objects
            metric_name: Metric name to filter by
            aggregation: Aggregation interval ('hour', 'day', 'minute')

        Returns:
            Dictionary with metric aggregations
        """
        if not self.client:
            return {}

        try:
            # Use materialized view if available
            if aggregation == 'hour':
                table = 'metrics_hourly'
                time_col = 'hour'
            else:
                table = 'metrics'
                time_col = 'timestamp'

            query = f"SELECT {time_col}, avg(value), max(value), min(value) FROM {table} WHERE 1=1"
            params = []

            if time_range:
                if time_range.get('start'):
                    query += f" AND {time_col} >= %s"
                    params.append(time_range['start'])
                if time_range.get('end'):
                    query += f" AND {time_col} <= %s"
                    params.append(time_range['end'])

            if metric_name:
                query += " AND metric_name = %s"
                params.append(metric_name)

            if aggregation != 'hour':
                if aggregation == 'day':
                    time_func = 'toStartOfDay'
                elif aggregation == 'minute':
                    time_func = 'toStartOfMinute'
                else:
                    time_func = 'toStartOfHour'

                query = f"""
                SELECT
                    {time_func}(timestamp) as time,
                    avg(value),
                    max(value),
                    min(value)
                FROM metrics
                WHERE 1=1
                """
                time_col = 'time'

            query += f" GROUP BY {time_col} ORDER BY {time_col}"

            result = self.client.query(query, params=params)
            return [
                {
                    'time': row[0],
                    'avg': row[1],
                    'max': row[2],
                    'min': row[3]
                }
                for row in result.result_rows
            ]
        except Exception as e:
            logger.error(f"Failed to get metric aggregations: {e}")
            return []

    def close(self):
        """Close the ClickHouse connection"""
        if self.client:
            try:
                self.client.disconnect()
            except Exception as e:
                logger.error(f"Failed to close ClickHouse connection: {e}")
            finally:
                self.client = None

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()

