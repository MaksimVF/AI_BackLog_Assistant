

"""
ClickHouse client for logs and metrics storage with Kafka integration
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

# Try to import Kafka
try:
    from confluent_kafka import Producer, KafkaException, KafkaError
    HAS_KAFKA = True
except ImportError:
    HAS_KAFKA = False

logger = logging.getLogger(__name__)

class ClickHouseClient:
    """ClickHouse client for storing and querying logs and metrics with Kafka integration"""

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize ClickHouse client with Kafka support

        Args:
            config: Configuration dictionary with ClickHouse and Kafka parameters
        """
        self.config = config or {}
        self.clickhouse_client = None
        self.kafka_producer = None
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize ClickHouse and Kafka clients from configuration"""
        self._initialize_clickhouse()
        self._initialize_kafka()

    def _initialize_clickhouse(self):
        """Initialize ClickHouse client from configuration"""
        if Client is None:
            logger.warning("clickhouse-connect not installed, using mock client")
            return

        # Load configuration from environment variables if not provided
        config = {
            'host': self.config.get('clickhouse_host') or self.config.get('host') or os.getenv('CLICKHOUSE_HOST', 'localhost'),
            'port': self.config.get('clickhouse_port') or self.config.get('port') or os.getenv('CLICKHOUSE_PORT', 8443),
            'username': self.config.get('clickhouse_username') or self.config.get('username') or os.getenv('CLICKHOUSE_USER', 'default'),
            'password': self.config.get('clickhouse_password') or self.config.get('password') or os.getenv('CLICKHOUSE_PASSWORD', ''),
            'database': self.config.get('clickhouse_database') or self.config.get('database') or os.getenv('CLICKHOUSE_DATABASE', 'ai_backlog_admin'),
            'secure': self.config.get('clickhouse_secure') or self.config.get('secure', True),
            'verify': self.config.get('clickhouse_verify') or self.config.get('verify', True),
            'ca_cert': self.config.get('clickhouse_ca_cert') or self.config.get('ca_cert') or os.getenv('CLICKHOUSE_CA_CERT'),
        }

        try:
            self.clickhouse_client = Client(**config)
            self._test_clickhouse_connection()
        except Exception as e:
            logger.error(f"Failed to initialize ClickHouse client: {e}")
            self.clickhouse_client = None

    def _initialize_kafka(self):
        """Initialize Kafka producer from configuration"""
        if not HAS_KAFKA:
            logger.warning("Kafka not available, using direct ClickHouse storage")
            return

        # Load Kafka configuration from environment variables if not provided
        kafka_config = {
            'bootstrap.servers': self.config.get('kafka_servers') or os.getenv('KAFKA_SERVERS', 'localhost:9092'),
            'client.id': self.config.get('kafka_client_id') or os.getenv('KAFKA_CLIENT_ID', 'ai-backlog-agent'),
            'security.protocol': self.config.get('kafka_security_protocol') or os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
            'sasl.mechanisms': self.config.get('kafka_sasl_mechanisms') or os.getenv('KAFKA_SASL_MECHANISMS', ''),
            'sasl.username': self.config.get('kafka_sasl_username') or os.getenv('KAFKA_SASL_USERNAME', ''),
            'sasl.password': self.config.get('kafka_sasl_password') or os.getenv('KAFKA_SASL_PASSWORD', ''),
        }

        # Remove empty SASL settings if not needed
        if not kafka_config['sasl.mechanisms']:
            kafka_config.pop('sasl.mechanisms', None)
            kafka_config.pop('sasl.username', None)
            kafka_config.pop('sasl.password', None)

        try:
            self.kafka_producer = Producer(kafka_config)
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            self.kafka_producer = None

    def _test_clickhouse_connection(self):
        """Test ClickHouse connection"""
        if not self.clickhouse_client:
            return False

        try:
            result = self.clickhouse_client.command('SELECT 1')
            return result == '1\n'
        except Exception as e:
            logger.error(f"ClickHouse connection test failed: {e}")
            return False

    def is_clickhouse_connected(self) -> bool:
        """Check if ClickHouse client is connected"""
        return self.clickhouse_client is not None

    def is_kafka_connected(self) -> bool:
        """Check if Kafka producer is available"""
        return self.kafka_producer is not None

    def is_connected(self) -> bool:
        """Check if either ClickHouse or Kafka is connected"""
        return self.is_clickhouse_connected() or self.is_kafka_connected()

    def _send_to_kafka(self, topic: str, message: Dict[str, Any]) -> bool:
        """
        Send a message to Kafka topic

        Args:
            topic: Kafka topic name
            message: Message to send as dictionary

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.kafka_producer:
            return False

        try:
            # Convert message to JSON string
            message_str = json.dumps(message).encode('utf-8')

            # Produce message to Kafka
            self.kafka_producer.produce(
                topic=topic,
                value=message_str,
                callback=self._kafka_delivery_callback
            )

            # Flush to ensure message is sent
            self.kafka_producer.flush()
            return True
        except Exception as e:
            logger.error(f"Failed to send message to Kafka topic {topic}: {e}")
            return False

    def _kafka_delivery_callback(self, err, msg):
        """Callback for Kafka message delivery"""
        if err:
            logger.error(f"Kafka message delivery failed: {err}")
        else:
            logger.debug(f"Kafka message delivered to {msg.topic()} [{msg.partition()}]")

    def _store_direct_to_clickhouse(self, table: str, data: Dict[str, Any], column_names: List[str]) -> bool:
        """
        Store data directly to ClickHouse

        Args:
            table: Table name
            data: Data to store as dictionary
            column_names: List of column names

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.clickhouse_client:
            return False

        try:
            # Convert data to list of values in the correct order
            values = [data[col] for col in column_names]

            # Insert into ClickHouse
            self.clickhouse_client.insert(table, [values], column_names=column_names)
            return True
        except Exception as e:
            logger.error(f"Failed to store data in ClickHouse table {table}: {e}")
            return False

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
        Store a log entry in ClickHouse (via Kafka if available)

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
        # Prepare log data
        timestamp = datetime.utcnow()

        if session_id and not isinstance(session_id, UUID):
            try:
                session_id = UUID(session_id)
            except ValueError:
                session_id = uuid4()

        if not session_id:
            session_id = uuid4()

        if metadata is None:
            metadata = {}

        # Prepare message for Kafka
        log_message = {
            "timestamp": timestamp.isoformat(),
            "level": level,
            "source": source,
            "message": message,
            "metadata": metadata,
            "agent_id": agent_id,
            "session_id": str(session_id),
            "message_type": "log"
        }

        # Try Kafka first if available
        if self.kafka_producer:
            if self._send_to_kafka("ai_backlog_logs", log_message):
                return True

        # Fallback to direct ClickHouse storage
        if self.clickhouse_client:
            try:
                # Convert metadata to JSON string for Map type
                metadata_str = json.dumps(metadata)

                values = [
                    (timestamp, level, source, message, metadata_str, agent_id, session_id)
                ]

                self.clickhouse_client.insert('logs', values, column_names=[
                    'timestamp', 'level', 'source', 'message', 'metadata', 'agent_id', 'session_id'
                ])

                return True
            except Exception as e:
                logger.error(f"Failed to store log: {e}")
                return False

        logger.warning("Neither Kafka nor ClickHouse is available, log not stored")
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
        Store a metric in ClickHouse (via Kafka if available)

        Args:
            metric_name: Name of the metric
            value: Metric value
            tags: Additional tags as dictionary
            agent_id: ID of the agent generating the metric
            session_id: Session ID

        Returns:
            bool: True if successful, False otherwise
        """
        # Prepare metric data
        timestamp = datetime.utcnow()

        if session_id and not isinstance(session_id, UUID):
            try:
                session_id = UUID(session_id)
            except ValueError:
                session_id = uuid4()

        if not session_id:
            session_id = uuid4()

        if tags is None:
            tags = {}

        # Prepare message for Kafka
        metric_message = {
            "timestamp": timestamp.isoformat(),
            "metric_name": metric_name,
            "value": value,
            "tags": tags,
            "agent_id": agent_id,
            "session_id": str(session_id),
            "message_type": "metric"
        }

        # Try Kafka first if available
        if self.kafka_producer:
            if self._send_to_kafka("ai_backlog_metrics", metric_message):
                return True

        # Fallback to direct ClickHouse storage
        if not self.clickhouse_client:
            return False

        try:
            # Convert tags to JSON string for Map type
            tags_str = json.dumps(tags)

            values = [
                (timestamp, metric_name, value, tags_str, agent_id, session_id)
            ]

            self.clickhouse_client.insert('metrics', values, column_names=[
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
        Store an event in ClickHouse (via Kafka if available)

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
        # Prepare event data
        timestamp = datetime.utcnow()

        if session_id and not isinstance(session_id, UUID):
            try:
                session_id = UUID(session_id)
            except ValueError:
                session_id = uuid4()

        if not session_id:
            session_id = uuid4()

        if metadata is None:
            metadata = {}

        # Prepare message for Kafka
        event_message = {
            "timestamp": timestamp.isoformat(),
            "event_type": event_type,
            "source": source,
            "details": details,
            "metadata": metadata,
            "agent_id": agent_id,
            "session_id": str(session_id),
            "message_type": "event"
        }

        # Try Kafka first if available
        if self.kafka_producer:
            if self._send_to_kafka("ai_backlog_events", event_message):
                return True

        # Fallback to direct ClickHouse storage
        if not self.clickhouse_client:
            return False

        try:
            # Convert metadata to JSON string for Map type
            metadata_str = json.dumps(metadata)

            values = [
                (timestamp, event_type, source, details, metadata_str, agent_id, session_id)
            ]

            self.clickhouse_client.insert('events', values, column_names=[
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

