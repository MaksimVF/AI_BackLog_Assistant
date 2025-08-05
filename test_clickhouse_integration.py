


"""
Test ClickHouse integration with LogCollectorAgent and MonitoringAgent
"""

import logging
import sys
import os
from datetime import datetime, timedelta
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.system_admin.log_collector_agent import LogCollectorAgent
from agents.system_admin.monitoring_agent import MonitoringAgent

def test_clickhouse_integration():
    """Test ClickHouse integration with system admin agents"""
    print("=== Testing ClickHouse Integration ===")

    # Test LogCollectorAgent
    print("\n1. Testing LogCollectorAgent with ClickHouse...")
    log_collector = LogCollectorAgent()

    # Check if ClickHouse is available
    if hasattr(log_collector, 'clickhouse_client') and log_collector.clickhouse_client:
        print("✅ ClickHouse client initialized successfully")
    else:
        print("⚠️  ClickHouse client not available, using in-memory logs only")

    # Collect some logs
    log_collector.collect_log("test_source", "info", "Test information message")
    log_collector.collect_log("test_source", "warning", "Test warning message")
    log_collector.collect_log("test_source", "error", "Test error message")

    # Test log querying
    print("\n2. Testing log querying...")
    logs = log_collector.query_logs(limit=10)
    print(f"   Found {len(logs)} logs in query")

    # Test log filtering
    error_logs = log_collector.filter_logs("ERROR")
    print(f"   Found {len(error_logs)} error logs")

    # Test log statistics
    stats = log_collector.get_log_stats()
    print(f"   Log statistics: {stats}")

    # Test MonitoringAgent
    print("\n3. Testing MonitoringAgent with ClickHouse...")
    monitoring_agent = MonitoringAgent()

    # Check if ClickHouse is available
    if hasattr(monitoring_agent, 'clickhouse_client') and monitoring_agent.clickhouse_client:
        print("✅ ClickHouse client initialized successfully")
    else:
        print("⚠️  ClickHouse client not available, metrics will not be persisted")

    # Get system status (this will also store metrics)
    system_status = monitoring_agent.get_system_status()
    print(f"   CPU usage: {system_status['cpu_percent']}%")
    print(f"   Memory usage: {system_status['memory']['percent']}%")
    print(f"   Disk usage: {system_status['disk']['percent']}%")

    # Test service status (this will also store events)
    service_status = monitoring_agent.check_service_status()
    print(f"   Service status: {service_status}")

    # Test metrics querying
    print("\n4. Testing metrics querying...")
    metrics = monitoring_agent.query_metrics(limit=10)
    print(f"   Found {len(metrics)} metrics")

    # Test metric aggregations
    print("\n5. Testing metric aggregations...")
    aggregations = monitoring_agent.get_metric_aggregations(aggregation='hour')
    print(f"   Found {len(aggregations)} aggregated metrics")

    # Test time range queries
    print("\n6. Testing time range queries...")
    time_range = {
        'start': datetime.utcnow() - timedelta(hours=1),
        'end': datetime.utcnow()
    }

    recent_logs = log_collector.query_logs(time_range=time_range)
    print(f"   Found {len(recent_logs)} logs in the last hour")

    recent_metrics = monitoring_agent.query_metrics(time_range=time_range)
    print(f"   Found {len(recent_metrics)} metrics in the last hour")

    print("\n=== ClickHouse Integration Test Completed ===")

if __name__ == "__main__":
    test_clickhouse_integration()

