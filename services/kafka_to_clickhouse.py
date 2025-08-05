


"""
Kafka to ClickHouse consumer service
"""

import os
import json
import logging
from datetime import datetime
from uuid import UUID
from typing import Dict, Any

from confluent_kafka import Consumer, KafkaException, KafkaError
from database.clickhouse_client import ClickHouseClient

logger = logging.getLogger(__name__)

class KafkaToClickHouseConsumer:
    """Service to consume messages from Kafka and store them in ClickHouse"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Kafka consumer and ClickHouse client

        Args:
            config: Configuration dictionary with Kafka and ClickHouse parameters
        """
        self.config = config or {}
        self.clickhouse_client = ClickHouseClient(self.config)
        self.kafka_consumer = self._initialize_kafka_consumer()

    def _initialize_kafka_consumer(self):
        """Initialize Kafka consumer from configuration"""
        kafka_config = {
            'bootstrap.servers': self.config.get('kafka_servers') or os.getenv('KAFKA_SERVERS', 'localhost:9092'),
            'group.id': self.config.get('kafka_group_id') or os.getenv('KAFKA_GROUP_ID', 'ai-backlog-clickhouse-consumer'),
            'auto.offset.reset': self.config.get('kafka_auto_offset_reset') or os.getenv('KAFKA_AUTO_OFFSET_RESET', 'earliest'),
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
            consumer = Consumer(kafka_config)
            logger.info("Kafka consumer initialized successfully")
            return consumer
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            return None

    def _process_log_message(self, message: Dict[str, Any]) -> bool:
        """Process a log message and store it in ClickHouse"""
        try:
            # Convert timestamp from ISO format
            timestamp = datetime.fromisoformat(message['timestamp'])

            # Convert session_id to UUID
            session_id = UUID(message['session_id']) if message['session_id'] else None

            # Store log in ClickHouse
            return self.clickhouse_client.store_log(
                level=message['level'],
                source=message['source'],
                message=message['message'],
                metadata=message.get('metadata', {}),
                agent_id=message.get('agent_id'),
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Failed to process log message: {e}")
            return False

    def _process_metric_message(self, message: Dict[str, Any]) -> bool:
        """Process a metric message and store it in ClickHouse"""
        try:
            # Convert timestamp from ISO format
            timestamp = datetime.fromisoformat(message['timestamp'])

            # Convert session_id to UUID
            session_id = UUID(message['session_id']) if message['session_id'] else None

            # Store metric in ClickHouse
            return self.clickhouse_client.store_metric(
                metric_name=message['metric_name'],
                value=message['value'],
                tags=message.get('tags', {}),
                agent_id=message.get('agent_id'),
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Failed to process metric message: {e}")
            return False

    def _process_event_message(self, message: Dict[str, Any]) -> bool:
        """Process an event message and store it in ClickHouse"""
        try:
            # Convert timestamp from ISO format
            timestamp = datetime.fromisoformat(message['timestamp'])

            # Convert session_id to UUID
            session_id = UUID(message['session_id']) if message['session_id'] else None

            # Store event in ClickHouse
            return self.clickhouse_client.store_event(
                event_type=message['event_type'],
                source=message['source'],
                details=message['details'],
                metadata=message.get('metadata', {}),
                agent_id=message.get('agent_id'),
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Failed to process event message: {e}")
            return False

    def _process_message(self, kafka_message):
        """Process a single Kafka message"""
        try:
            # Parse message value
            message = json.loads(kafka_message.value().decode('utf-8'))

            # Determine message type and process accordingly
            message_type = message.get('message_type')

            if message_type == 'log':
                success = self._process_log_message(message)
            elif message_type == 'metric':
                success = self._process_metric_message(message)
            elif message_type == 'event':
                success = self._process_event_message(message)
            else:
                logger.warning(f"Unknown message type: {message_type}")
                success = False

            if success:
                logger.debug(f"Successfully processed {message_type} message")
            else:
                logger.error(f"Failed to process {message_type} message")

        except Exception as e:
            logger.error(f"Failed to process Kafka message: {e}")

    def consume_messages(self, topics: list = None, timeout: float = 1.0):
        """
        Consume messages from Kafka topics and store them in ClickHouse

        Args:
            topics: List of topics to consume from
            timeout: Poll timeout in seconds
        """
        if not topics:
            topics = ['ai_backlog_logs', 'ai_backlog_metrics', 'ai_backlog_events']

        if not self.kafka_consumer:
            logger.error("Kafka consumer not initialized")
            return

        try:
            # Subscribe to topics
            self.kafka_consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")

            while True:
                # Poll for messages
                msg = self.kafka_consumer.poll(timeout=timeout)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:
                        logger.error(f"Kafka error: {msg.error()}")
                        continue

                # Process the message
                self._process_message(msg)

        except KeyboardInterrupt:
            logger.info("Kafka consumer stopped")
        except Exception as e:
            logger.error(f"Kafka consumer error: {e}")
        finally:
            # Cleanup on exit
            self.kafka_consumer.close()
            logger.info("Kafka consumer closed")

def run_kafka_consumer():
    """Run the Kafka to ClickHouse consumer service"""
    # Load configuration from environment variables
    config = {
        'kafka_servers': os.getenv('KAFKA_SERVERS'),
        'kafka_group_id': os.getenv('KAFKA_GROUP_ID'),
        'kafka_auto_offset_reset': os.getenv('KAFKA_AUTO_OFFSET_RESET'),
        'kafka_security_protocol': os.getenv('KAFKA_SECURITY_PROTOCOL'),
        'kafka_sasl_mechanisms': os.getenv('KAFKA_SASL_MECHANISMS'),
        'kafka_sasl_username': os.getenv('KAFKA_SASL_USERNAME'),
        'kafka_sasl_password': os.getenv('KAFKA_SASL_PASSWORD'),
        'clickhouse_host': os.getenv('CLICKHOUSE_HOST'),
        'clickhouse_port': os.getenv('CLICKHOUSE_PORT'),
        'clickhouse_username': os.getenv('CLICKHOUSE_USER'),
        'clickhouse_password': os.getenv('CLICKHOUSE_PASSWORD'),
        'clickhouse_database': os.getenv('CLICKHOUSE_DATABASE'),
    }

    # Initialize and run consumer
    consumer = KafkaToClickHouseConsumer(config)
    consumer.consume_messages()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run the consumer
    run_kafka_consumer()


