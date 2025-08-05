


# Kafka Integration for AI Backlog Assistant

## Overview

This document describes the Kafka integration for the AI Backlog Assistant system. Kafka is used as an intermediate buffer between the agents and ClickHouse to provide better reliability, scalability, and fault tolerance.

## Architecture

```
[Agents] → [Kafka Topics] → [Kafka Consumer Service] → [ClickHouse]
     ↑                          ↑                          ↑
   Produce                    Consume                   Store
```

## Components

### 1. Kafka Producer (in ClickHouseClient)

The `ClickHouseClient` class now includes Kafka producer capabilities. When agents call methods like `store_log()`, `store_metric()`, or `store_event()`, the client first attempts to send the data to Kafka topics. If Kafka is unavailable, it falls back to direct ClickHouse storage.

### 2. Kafka Topics

Three Kafka topics are used:
- `ai_backlog_logs`: For log messages
- `ai_backlog_metrics`: For metric data
- `ai_backlog_events`: For event data

### 3. Kafka Consumer Service

The `KafkaToClickHouseConsumer` service consumes messages from Kafka topics and writes them to ClickHouse. This service runs independently and ensures that all data in Kafka is eventually stored in ClickHouse.

## Configuration

### Environment Variables

The following environment variables are used for Kafka configuration:

- `KAFKA_SERVERS`: Kafka bootstrap servers (default: `localhost:9092`)
- `KAFKA_GROUP_ID`: Consumer group ID (default: `ai-backlog-clickhouse-consumer`)
- `KAFKA_AUTO_OFFSET_RESET`: Offset reset policy (default: `earliest`)
- `KAFKA_SECURITY_PROTOCOL`: Security protocol (default: `PLAINTEXT`)
- `KAFKA_SASL_MECHANISMS`: SASL mechanisms (optional)
- `KAFKA_SASL_USERNAME`: SASL username (optional)
- `KAFKA_SASL_PASSWORD`: SASL password (optional)

### ClickHouse Configuration

The same ClickHouse configuration is used for both the producer and consumer:
- `CLICKHOUSE_HOST`
- `CLICKHOUSE_PORT`
- `CLICKHOUSE_USER`
- `CLICKHOUSE_PASSWORD`
- `CLICKHOUSE_DATABASE`

## Deployment

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Kafka Consumer Service

```bash
python services/kafka_to_clickhouse.py
```

### 3. Configure Agents

Ensure that agents are configured to use the ClickHouse client with Kafka support:

```python
from database.clickhouse_client import ClickHouseClient

# Initialize client with Kafka and ClickHouse configuration
client = ClickHouseClient({
    'kafka_servers': 'your-kafka-servers',
    'clickhouse_host': 'your-clickhouse-host',
    # ... other configuration
})
```

## Benefits

### 1. Reliability

- Data is first written to Kafka, which provides durable storage
- Even if ClickHouse is temporarily unavailable, data is preserved in Kafka
- The consumer service will process messages when ClickHouse becomes available

### 2. Scalability

- Kafka can handle high-throughput data streams
- Multiple consumer instances can be run for load balancing
- Horizontal scaling is supported

### 3. Fault Tolerance

- Kafka provides message retention and replay capabilities
- Failed messages can be retried or sent to dead-letter queues
- System can recover from temporary outages

### 4. Decoupling

- Producers (agents) are decoupled from consumers (ClickHouse)
- Each component can be scaled and maintained independently
- Schema changes can be handled more gracefully

## Monitoring

### Kafka Metrics

Monitor the following Kafka metrics:
- Message production rate
- Message consumption rate
- Topic lag (difference between produced and consumed messages)
- Consumer group health

### ClickHouse Metrics

Monitor the following ClickHouse metrics:
- Insertion rate
- Query performance
- Disk usage
- Table sizes

## Troubleshooting

### Common Issues

1. **Kafka Connection Errors**: Check network connectivity and Kafka server status
2. **ClickHouse Connection Errors**: Verify ClickHouse credentials and network access
3. **Message Processing Failures**: Check consumer logs for detailed error messages
4. **High Topic Lag**: May indicate consumer performance issues or ClickHouse bottlenecks

### Logs

- Producer logs: Available in the agent logs
- Consumer logs: Available in the Kafka consumer service logs
- Kafka broker logs: Check Kafka server logs for broker-side issues

## Future Enhancements

1. **Dead-Letter Queue**: Implement DLQ for failed message processing
2. **Message Retries**: Add retry logic with exponential backoff
3. **Monitoring Integration**: Add Prometheus/Grafana monitoring
4. **Schema Validation**: Validate message schemas before processing
5. **Compression**: Enable message compression for better throughput

## Conclusion

The Kafka integration provides a robust, scalable, and fault-tolerant solution for data ingestion into ClickHouse. By decoupling data producers from consumers, the system can handle higher loads and recover from failures more gracefully.

