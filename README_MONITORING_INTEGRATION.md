

# Monitoring and Logging Integration Guide

## Overview

This document describes the comprehensive monitoring and logging integration for the AI_BackLog_Assistant system. The integration includes:

1. **Centralized Logging** (ELK stack)
2. **Application Performance Monitoring** (APM)
3. **Health Check Endpoints**
4. **System Metrics Collection**

## Components

### 1. Centralized Logging (ELK Stack)

The system uses an enhanced logging system with ELK stack integration:

- **E**lasticsearch: For log storage and search
- **L**ogstash: For log processing (optional)
- **K**ibana: For log visualization

#### Configuration

The logging configuration is defined in `config/logging_config.yaml`:

```yaml
external_systems:
  elk:
    host: "localhost:9200"
    index: "ai_backlog_logs"
    username: "elastic"
    password: "changeme"
```

#### Usage

The logging system is initialized in the main application:

```python
from agents.system_admin.logging_manager import initialize_logging

logging_manager = initialize_logging(
    service_name="AI_BackLog_Assistant",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()
```

### 2. Application Performance Monitoring (APM)

The system collects comprehensive performance metrics:

- **CPU Usage**: Percentage, load averages, core counts
- **Memory Usage**: Virtual and swap memory statistics
- **Disk Usage**: Usage percentages, I/O operations
- **Network Metrics**: Bytes sent/received, packet statistics
- **Process Metrics**: Count and top resource consumers

#### Monitoring Agent

The `MonitoringAgent` collects and stores metrics:

```python
from agents.system_admin.monitoring_agent import MonitoringAgent

monitoring_agent = MonitoringAgent()
status = monitoring_agent.get_system_status()
```

### 3. Health Check Endpoints

The API server provides standard health check endpoints:

- **`/health`**: Comprehensive health status
- **`/ready`**: Readiness status for orchestration
- **`/status`**: Detailed system status
- **`/metrics`**: System metrics

#### Example Health Response

```json
{
  "status": "healthy",
  "timestamp": "2025-08-09T12:34:56.789012",
  "system": {
    "cpu_usage": 15.2,
    "memory_usage": 42.8,
    "disk_usage": 33.5,
    "uptime_seconds": 3600
  },
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "llm_provider": "healthy",
    "queue": "healthy"
  },
  "alerts": []
}
```

### 4. System Metrics Collection

Metrics are collected and stored in ClickHouse for historical analysis:

- **CPU Metrics**: `system.cpu_percent`, `system.cpu_user`, etc.
- **Memory Metrics**: `system.memory.used`, `system.memory.free`
- **Disk Metrics**: `system.disk.used`, `system.disk.free`
- **Network Metrics**: `system.network.bytes_sent`, `system.network.bytes_recv`

## Integration Status

### ✅ Implemented Features

1. **Enhanced Logging System**
   - Structured JSON logging
   - Log rotation and archiving
   - ELK stack integration
   - Specialized logging (metrics, audits, health checks)

2. **Comprehensive Monitoring**
   - Detailed system metrics collection
   - ClickHouse integration for metric storage
   - Multi-level alert system
   - Service status monitoring

3. **Health Check Endpoints**
   - Standard `/health` and `/ready` endpoints
   - Detailed system status API
   - Metrics endpoint

4. **Background Monitoring**
   - Continuous system monitoring
   - Periodic status logging
   - Alert detection

### 🔄 Partially Implemented

1. **ELK Integration**
   - Configuration is complete
   - Requires Elasticsearch server to be running

2. **APM Visualization**
   - Metrics are collected
   - Visualization requires Kibana/Grafana setup

## Setup Instructions

### 1. Start Elasticsearch

```bash
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.10.0
```

### 2. Start Kibana

```bash
docker run -d --name kibana --link elasticsearch:elasticsearch -p 5601:5601 kibana:8.10.0
```

### 3. Run the API Server

```bash
python api_server.py
```

### 4. Access Health Endpoints

- Health: `http://localhost:8000/health`
- Readiness: `http://localhost:8000/ready`
- Status: `http://localhost:8000/status`
- Metrics: `http://localhost:8000/metrics`

### 5. View Logs in Kibana

1. Open Kibana: `http://localhost:5601`
2. Go to "Discover" and select the `ai_backlog_logs` index
3. Explore the structured logs

## Future Enhancements

1. **Complete ELK Integration**
   - Add Logstash for log processing
   - Implement log enrichment

2. **APM Dashboard**
   - Create Kibana dashboards for system metrics
   - Add Grafana for advanced visualization

3. **Alert Notifications**
   - Integrate with alerting systems (PagerDuty, Opsgenie)
   - Add email/SMS notifications

4. **Distributed Tracing**
   - Integrate with OpenTelemetry
   - Add trace context to logs

## Conclusion

The monitoring and logging integration provides comprehensive observability for the AI_BackLog_Assistant system. The implementation includes centralized logging with ELK stack, detailed system metrics collection, health check endpoints, and background monitoring.

To fully utilize the integration:
1. Start the ELK stack (Elasticsearch + Kibana)
2. Run the API server with monitoring
3. Access the health endpoints
4. View logs and metrics in Kibana

The system is now ready for production deployment with proper monitoring and logging capabilities.

