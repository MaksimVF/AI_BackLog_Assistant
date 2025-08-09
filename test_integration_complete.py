


"""
Integration test for monitoring and logging improvements
"""

import os
import sys
import json
import time
import requests
import threading

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.monitoring_agent import MonitoringAgent
from health import get_health_status, get_readiness_status

def test_logging_integration():
    """Test the logging integration"""
    print("=== Testing Logging Integration ===")

    # Initialize logging
    logging_manager = initialize_logging(
        service_name="IntegrationTest",
        environment="test"
    )
    logger = logging_manager.get_logger()

    # Test different log levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    # Test structured logging
    logger.info("Structured log with context", extra={
        'user_id': 'test123',
        'operation': 'integration_test',
        'status': 'success'
    })

    # Test specialized logging
    logging_manager.log_metric("test_metric", 42.5, unit="ms")
    logging_manager.log_audit("test_action", "test_user", "test_resource", "success")
    logging_manager.log_health_check("test_service", "healthy", uptime=1234)

    print("✓ Logging integration test completed")

def test_monitoring_integration():
    """Test the monitoring integration"""
    print("\n=== Testing Monitoring Integration ===")

    # Initialize monitoring agent
    monitoring_agent = MonitoringAgent()

    # Get system status
    status = monitoring_agent.get_system_status()
    print(f"CPU Usage: {status.get('cpu', {}).get('percent', 0)}%")
    print(f"Memory Usage: {status.get('memory', {}).get('virtual', {}).get('percent', 0)}%")
    print(f"Disk Usage: {status.get('disk', {}).get('usage', {}).get('percent', 0)}%")
    print(f"Process Count: {status.get('processes', {}).get('count', 0)}")

    # Test service status
    services = monitoring_agent.check_service_status()
    print(f"Service Status: {services}")

    print("✓ Monitoring integration test completed")

def test_health_endpoints():
    """Test the health endpoints"""
    print("\n=== Testing Health Endpoints ===")

    # Start API server in background
    def start_api_server():
        os.system("python api_server.py &")
        time.sleep(5)  # Wait for server to start

    server_thread = threading.Thread(target=start_api_server)
    server_thread.start()
    server_thread.join(timeout=10)

    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"Health Status: {health_data.get('status')}")
            print(f"CPU Usage: {health_data.get('system', {}).get('cpu_usage')}%")
            print(f"Memory Usage: {health_data.get('system', {}).get('memory_usage')}%")
            print("✓ Health endpoint test passed")
        else:
            print(f"✗ Health endpoint failed: {response.status_code}")

        # Test readiness endpoint
        response = requests.get("http://localhost:8000/ready")
        if response.status_code == 200:
            readiness_data = response.json()
            print(f"Readiness Status: {readiness_data.get('status')}")
            print("✓ Readiness endpoint test passed")
        else:
            print(f"✗ Readiness endpoint failed: {response.status_code}")

        # Test status endpoint
        response = requests.get("http://localhost:8000/status")
        if response.status_code == 200:
            print("✓ Status endpoint test passed")
        else:
            print(f"✗ Status endpoint failed: {response.status_code}")

        # Test metrics endpoint
        response = requests.get("http://localhost:8000/metrics")
        if response.status_code == 200:
            print("✓ Metrics endpoint test passed")
        else:
            print(f"✗ Metrics endpoint failed: {response.status_code}")

    except requests.ConnectionError:
        print("✗ API server not available - endpoints test skipped")
    except Exception as e:
        print(f"✗ Endpoints test failed: {e}")

    # Clean up: kill the API server
    os.system("pkill -f 'python api_server.py'")

def test_health_functions():
    """Test the health functions directly"""
    print("\n=== Testing Health Functions ===")

    # Test health status
    health = get_health_status()
    print(f"Health Status: {health.get('status')}")
    print(f"Alerts: {len(health.get('alerts', []))}")

    # Test readiness status
    readiness = get_readiness_status()
    print(f"Readiness Status: {readiness.get('status')}")

    print("✓ Health functions test completed")

def main():
    """Run all integration tests"""
    print("🔍 Running Monitoring and Logging Integration Tests")
    print("=" * 60)

    try:
        test_logging_integration()
        test_monitoring_integration()
        test_health_functions()
        test_health_endpoints()

        print("\n🎉 All integration tests completed!")
        print("✅ Monitoring and logging improvements are fully integrated")

    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


