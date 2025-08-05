


# ClickHouse Integration for Logs and Metrics

This document describes the ClickHouse integration for persistent storage and analysis of logs and metrics in the AI Backlog Assistant system.

## Overview

ClickHouse is used as a high-performance, scalable storage solution for:

1. **Logs**: System logs, error logs, and event logs
2. **Metrics**: System performance metrics and service health metrics
3. **Events**: System events and service status changes

## Architecture

```
[Agents] → [ClickHouse Client] → [ClickHouse Database]
     ↑                          ↑
    Query                      Store
```

## Schema Design

### Tables

1. **logs**: Stores log entries with timestamp, level, source, message, and metadata
2. **metrics**: Stores metric data points with timestamp, metric name, value, and tags
3. **events**: Stores system events with timestamp, event type, source, and details

### Materialized Views

1. **logs_by_level**: Aggregates log counts by level and minute
2. **metrics_hourly**: Provides hourly aggregations (avg, max, min) for metrics

## Configuration

ClickHouse configuration is loaded from environment variables:

- `CLICKHOUSE_HOST`: ClickHouse server host (default: localhost)
- `CLICKHOUSE_PORT`: ClickHouse server port (default: 8443)
- `CLICKHOUSE_USER`: ClickHouse username (default: default)
- `CLICKHOUSE_PASSWORD`: ClickHouse password
- `CLICKHOUSE_DATABASE`: ClickHouse database name (default: ai_backlog_admin)
- `CLICKHOUSE_SECURE`: Use secure connection (default: true)
- `CLICKHOUSE_CA_CERT`: Path to CA certificate for secure connections

## Integration Points

### LogCollectorAgent

- Stores all collected logs in ClickHouse
- Provides query capabilities for historical log analysis
- Maintains in-memory logs as fallback when ClickHouse is unavailable

### MonitoringAgent

- Stores system metrics (CPU, memory, disk, uptime) in ClickHouse
- Stores service status events in ClickHouse
- Provides query capabilities for historical metric analysis

## Usage Examples

### Storing Logs

```python
log_collector = LogCollectorAgent()
log_collector.collect_log(
    source="system_monitor",
    level="warning",
    message="High CPU usage detected",
    context={"cpu_percent": 95, "threshold": 90}
)
```

### Querying Logs

```python
# Get recent error logs
logs = log_collector.query_logs(
    level="ERROR",
    time_range={
        'start': datetime.utcnow() - timedelta(hours=1),
        'end': datetime.utcnow()
    }
)

# Get log statistics
stats = log_collector.get_log_stats()
```

### Storing Metrics

```python
monitoring_agent = MonitoringAgent()
status = monitoring_agent.get_system_status()  # Automatically stores metrics
```

### Querying Metrics

```python
# Get CPU metrics for the last day
metrics = monitoring_agent.query_metrics(
    metric_name="system.cpu_percent",
    time_range={
        'start': datetime.utcnow() - timedelta(days=1),
        'end': datetime.utcnow()
    }
)

# Get hourly aggregations
aggregations = monitoring_agent.get_metric_aggregations(aggregation='hour')
```

## Benefits

1. **Performance**: ClickHouse handles high-volume data ingestion efficiently
2. **Compression**: Excellent storage efficiency with ZSTD compression
3. **Scalability**: Can scale horizontally as data volume grows
4. **Analytics**: Optimized for analytical queries and aggregations
5. **Reliability**: Data persistence with automatic retention policies

## Fallback Behavior

When ClickHouse is unavailable:
- Agents continue to function using in-memory storage
- Logs and metrics are stored locally
- No data is lost (though persistence is limited to the agent's lifetime)

## Monitoring and Maintenance

### Health Monitoring

Regularly check:
- ClickHouse cluster health
- Data ingestion rates
- Query performance
- Disk usage and retention policies

### Retention Policies

Configure TTL settings based on data volume and retention needs:
- Logs: 6 months (configurable)
- Metrics: 2 years (configurable)
- Events: 1 year (configurable)

## Deployment

### Prerequisites

1. ClickHouse server (version 22.8+ recommended)
2. Python 3.8+
3. Required packages: `clickhouse-connect`

### Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables for ClickHouse connection
3. Initialize database schema (run `database/clickhouse_schema.sql`)

### Testing

Run the integration test:
```bash
python test_clickhouse_integration.py
```

## Future Enhancements

1. **Alerting**: Add anomaly detection and alerting based on metrics
2. **Dashboards**: Integrate with visualization tools like Grafana
3. **Export**: Add data export capabilities for compliance
4. **Sharding**: Implement distributed storage for large-scale deployments

## Troubleshooting

### Common Issues

1. **Connection Errors**: Check network connectivity and credentials
2. **Permission Errors**: Verify ClickHouse user has appropriate permissions
3. **Performance Issues**: Optimize queries and check partition setup
4. **Data Loss**: Verify retention policies and backup configuration

### Debugging

Enable debug logging for detailed troubleshooting:
```python
logging.getLogger('clickhouse_connect').setLevel(logging.DEBUG)
```

## Conclusion

The ClickHouse integration provides a robust, scalable solution for long-term storage and analysis of system logs and metrics, enabling comprehensive monitoring, diagnostics, and historical analysis capabilities for the AI Backlog Assistant system.

