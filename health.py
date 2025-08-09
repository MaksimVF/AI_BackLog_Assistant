
"""
Health check module for AI_BackLog_Assistant
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.system_admin.monitoring_agent import MonitoringAgent
from agents.system_admin.logging_manager import initialize_logging

# Initialize logging
logging_manager = initialize_logging(
    service_name="HealthCheck",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

def get_health_status() -> Dict[str, Any]:
    """
    Get comprehensive health status of the system

    Returns:
        Dictionary containing health status information
    """
    try:
        # Get system status from monitoring agent
        system_status = monitoring_agent.get_system_status()

        # Check critical components
        critical_services = {
            "database": check_database(),
            "cache": check_cache(),
            "llm_provider": check_llm_provider(),
            "queue": check_queue()
        }

        # Check for any critical alerts
        alerts = []
        system_info = system_status.get('system_status', {}).get('system', {})

        # CPU check
        cpu_usage = system_info.get('cpu', {}).get('percent', 0)
        if cpu_usage > 90:
            alerts.append({
                'type': 'critical',
                'message': f'High CPU usage: {cpu_usage}%',
                'component': 'system'
            })

        # Memory check
        memory_usage = system_info.get('memory', {}).get('virtual', {}).get('percent', 0)
        if memory_usage > 90:
            alerts.append({
                'type': 'critical',
                'message': f'High memory usage: {memory_usage}%',
                'component': 'system'
            })

        # Disk check
        disk_usage = system_info.get('disk', {}).get('usage', {}).get('percent', 0)
        if disk_usage > 90:
            alerts.append({
                'type': 'critical',
                'message': f'High disk usage: {disk_usage}%',
                'component': 'system'
            })

        # Service checks
        for service, status in critical_services.items():
            if status != 'healthy':
                alerts.append({
                    'type': 'critical',
                    'message': f'Service {service} is {status}',
                    'component': service
                })

        # Determine overall health
        overall_status = 'healthy' if not alerts else 'degraded'

        health_status = {
            'status': overall_status,
            'timestamp': datetime.utcnow().isoformat(),
            'system': {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'uptime_seconds': system_info.get('uptime_seconds', 0)
            },
            'services': critical_services,
            'alerts': alerts,
            'details': system_status
        }

        return health_status

    except Exception as e:
        logger.error(f"Failed to get health status: {e}")
        return {
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }

def check_database() -> str:
    """Check database connectivity"""
    try:
        # In a real implementation, this would actually check the database
        # For now, return a mock status
        return 'healthy'
    except Exception as e:
        logger.error(f"Database check failed: {e}")
        return 'unhealthy'

def check_cache() -> str:
    """Check cache system connectivity"""
    try:
        # In a real implementation, this would actually check the cache
        return 'healthy'
    except Exception as e:
        logger.error(f"Cache check failed: {e}")
        return 'unhealthy'

def check_llm_provider() -> str:
    """Check LLM provider connectivity"""
    try:
        # In a real implementation, this would actually check the LLM provider
        return 'healthy'
    except Exception as e:
        logger.error(f"LLM provider check failed: {e}")
        return 'unhealthy'

def check_queue() -> str:
    """Check queue system connectivity"""
    try:
        # In a real implementation, this would actually check the queue
        return 'healthy'
    except Exception as e:
        logger.error(f"Queue check failed: {e}")
        return 'unhealthy'

def get_readiness_status() -> Dict[str, Any]:
    """
    Get readiness status for the application

    Returns:
        Dictionary containing readiness status
    """
    try:
        # Check if all critical services are ready
        services = {
            'database': check_database(),
            'cache': check_cache(),
            'llm_provider': check_llm_provider(),
            'queue': check_queue()
        }

        # Check if system resources are sufficient
        system_status = monitoring_agent.get_system_status()
        system_info = system_status.get('system_status', {}).get('system', {})

        cpu_usage = system_info.get('cpu', {}).get('percent', 0)
        memory_usage = system_info.get('memory', {}).get('virtual', {}).get('percent', 0)
        disk_usage = system_info.get('disk', {}).get('usage', {}).get('percent', 0)

        # Determine readiness
        all_services_ready = all(status == 'healthy' for status in services.values())
        resources_sufficient = (cpu_usage < 85) and (memory_usage < 85) and (disk_usage < 85)

        overall_readiness = 'ready' if (all_services_ready and resources_sufficient) else 'not_ready'

        return {
            'status': overall_readiness,
            'timestamp': datetime.utcnow().isoformat(),
            'services': services,
            'system': {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage
            }
        }

    except Exception as e:
        logger.error(f"Failed to get readiness status: {e}")
        return {
            'status': 'not_ready',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }

if __name__ == "__main__":
    # Test the health check
    print("Testing health check module...")
    health = get_health_status()
    print(f"Health status: {health['status']}")
    print(f"CPU usage: {health['system']['cpu_usage']}%")
    print(f"Memory usage: {health['system']['memory_usage']}%")
    print(f"Disk usage: {health['system']['disk_usage']}%")

    readiness = get_readiness_status()
    print(f"Readiness status: {readiness['status']}")
