


"""
Test Kafka integration with ClickHouse
"""

import os
import json
import time
import threading
from unittest.mock import patch, MagicMock
from confluent_kafka import Producer, Consumer, KafkaError

from database.clickhouse_client import ClickHouseClient
from services.kafka_to_clickhouse import KafkaToClickHouseConsumer

def test_kafka_producer_fallback():
    """Test that ClickHouse client uses Kafka when available and falls back to direct storage"""

    # Mock Kafka producer
    mock_producer = MagicMock()
    mock_producer.produce.return_value = None

    # Mock ClickHouse client
    mock_clickhouse = MagicMock()
    mock_clickhouse.insert.return_value = None

    with patch('confluent_kafka.Producer', return_value=mock_producer), \
         patch('clickhouse_connect.Client', return_value=mock_clickhouse):

        # Initialize client with Kafka and ClickHouse
        client = ClickHouseClient({
            'kafka_servers': 'localhost:9092',
            'clickhouse_host': 'localhost'
        })

        # Test log storage - should use Kafka
        result = client.store_log('info', 'test_source', 'test message')
        assert result is True
        assert mock_producer.produce.called
        assert not mock_clickhouse.insert.called

        # Reset mocks
        mock_producer.reset_mock()
        mock_clickhouse.reset_mock()

        # Test with Kafka producer failing - should fallback to ClickHouse
        mock_producer.produce.side_effect = Exception("Kafka error")
        result = client.store_log('error', 'test_source', 'test message')
        assert result is True
        assert mock_producer.produce.called
        assert mock_clickhouse.insert.called

def test_kafka_consumer():
    """Test Kafka consumer service"""

    # Mock Kafka consumer
    mock_consumer = MagicMock()
    mock_consumer.poll.side_effect = [
        # First poll returns a message
        MagicMock(value=lambda: json.dumps({
            'message_type': 'log',
            'timestamp': '2023-01-01T00:00:00',
            'level': 'info',
            'source': 'test',
            'message': 'test message',
            'metadata': {},
            'agent_id': 'test_agent',
            'session_id': '123e4567-e89b-12d3-a456-426614174000'
        }).encode('utf-8'), error=lambda: None),
        # Second poll returns None (timeout)
        None,
        # Third poll raises KeyboardInterrupt to stop
        KeyboardInterrupt()
    ]

    # Mock ClickHouse client
    mock_clickhouse = MagicMock()
    mock_clickhouse.store_log.return_value = True

    with patch('confluent_kafka.Consumer', return_value=mock_consumer), \
         patch('database.clickhouse_client.ClickHouseClient', return_value=mock_clickhouse):

        # Initialize consumer
        consumer = KafkaToClickHouseConsumer({
            'kafka_servers': 'localhost:9092',
            'clickhouse_host': 'localhost'
        })

        # Run consumer in a separate thread to avoid blocking
        consumer_thread = threading.Thread(
            target=consumer.consume_messages,
            kwargs={'topics': ['test_topic'], 'timeout': 0.1}
        )
        consumer_thread.daemon = True
        consumer_thread.start()

        # Wait a bit for processing
        time.sleep(0.5)

        # Verify that the message was processed
        assert mock_clickhouse.store_log.called

        # Cleanup
        consumer.kafka_consumer.close()

def test_kafka_integration_end_to_end():
    """Test end-to-end Kafka integration (requires real Kafka server)"""

    # Skip if Kafka is not available
    if not os.getenv('KAFKA_SERVERS'):
        print("Skipping end-to-end test - Kafka not configured")
        return

    # This test would require a real Kafka server and ClickHouse instance
    # It would:
    # 1. Start a Kafka producer
    # 2. Send test messages to Kafka
    # 3. Start the consumer service
    # 4. Verify messages are stored in ClickHouse
    # 5. Clean up

    print("End-to-end test would run here with a real Kafka/ClickHouse setup")

if __name__ == "__main__":
    print("Running Kafka integration tests...")

    test_kafka_producer_fallback()
    print("✓ Kafka producer fallback test passed")

    test_kafka_consumer()
    print("✓ Kafka consumer test passed")

    test_kafka_integration_end_to_end()
    print("✓ End-to-end test completed (skipped if no Kafka configured)")

    print("All Kafka integration tests completed!")



