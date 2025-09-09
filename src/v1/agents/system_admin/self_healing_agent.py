
import sys
import os
import time
import logging
import psutil
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseAgent
from .notification_agent import NotificationAgent
from .monitoring_agent import MonitoringAgent

class SelfHealingAgent(BaseAgent):
    """
    SelfHealingAgent - Automatically detects and resolves system issues
    based on monitoring data and predefined recovery strategies.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(name="SelfHealingAgent")
        self.config = config or {}
        self.logger = logging.getLogger("SelfHealingAgent")
        self.notifier = NotificationAgent()
        self.monitor = MonitoringAgent()

        # Default thresholds for self-healing actions
        self.thresholds = {
            'cpu_critical': self.config.get('cpu_critical', 95.0),
            'memory_critical': self.config.get('memory_critical', 95.0),
            'disk_critical': self.config.get('disk_critical', 90.0),
            'process_count_max': self.config.get('process_count_max', 1000),
            'cache_cleanup_interval': self.config.get('cache_cleanup_interval', 86400),  # 24 hours
            'temp_file_cleanup_interval': self.config.get('temp_file_cleanup_interval', 43200)  # 12 hours
        }

        # Track last cleanup times
        self.last_cleanup = {
            'cache': 0,
            'temp_files': 0
        }

        self.logger.info("SelfHealingAgent initialized with self-recovery capabilities")

    def check_system_health(self) -> Dict[str, Any]:
        """Check system health and determine if self-healing actions are needed"""
        system_status = self.monitor.get_system_status()
        current_time = time.time()

        # Analyze system status and determine actions
        actions_needed = []

        # CPU analysis
        cpu_usage = system_status.get('cpu', {}).get('percent', 0)
        if cpu_usage > self.thresholds['cpu_critical']:
            actions_needed.append({
                'type': 'cpu_optimization',
                'priority': 'critical',
                'details': f"CPU usage at {cpu_usage}% exceeds critical threshold"
            })

        # Memory analysis
        memory_usage = system_status.get('memory', {}).get('virtual', {}).get('percent', 0)
        if memory_usage > self.thresholds['memory_critical']:
            actions_needed.append({
                'type': 'memory_optimization',
                'priority': 'critical',
                'details': f"Memory usage at {memory_usage}% exceeds critical threshold"
            })

        # Disk analysis
        disk_usage = system_status.get('disk', {}).get('usage', {}).get('percent', 0)
        if disk_usage > self.thresholds['disk_critical']:
            actions_needed.append({
                'type': 'disk_optimization',
                'priority': 'critical',
                'details': f"Disk usage at {disk_usage}% exceeds critical threshold"
            })

        # Process count analysis
        process_count = system_status.get('processes', {}).get('count', 0)
        if process_count > self.thresholds['process_count_max']:
            actions_needed.append({
                'type': 'process_optimization',
                'priority': 'warning',
                'details': f"Process count {process_count} exceeds maximum threshold"
            })

        # Check if cache cleanup is needed
        if (current_time - self.last_cleanup['cache']) > self.thresholds['cache_cleanup_interval']:
            actions_needed.append({
                'type': 'cache_cleanup',
                'priority': 'maintenance',
                'details': "Scheduled cache cleanup"
            })

        # Check if temp file cleanup is needed
        if (current_time - self.last_cleanup['temp_files']) > self.thresholds['temp_file_cleanup_interval']:
            actions_needed.append({
                'type': 'temp_file_cleanup',
                'priority': 'maintenance',
                'details': "Scheduled temporary file cleanup"
            })

        return {
            'system_status': system_status,
            'actions_needed': actions_needed,
            'timestamp': datetime.utcnow().isoformat()
        }

    def perform_self_healing(self, actions: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """Perform self-healing actions based on detected issues"""
        if actions is None:
            health_check = self.check_system_health()
            actions = health_check['actions_needed']

        results = []
        current_time = time.time()

        for action in actions:
            action_type = action['type']
            priority = action['priority']
            details = action['details']

            self.logger.info(f"Performing self-healing action: {action_type} (priority: {priority})")

            try:
                if action_type == 'cpu_optimization':
                    result = self._optimize_cpu()
                elif action_type == 'memory_optimization':
                    result = self._optimize_memory()
                elif action_type == 'disk_optimization':
                    result = self._optimize_disk()
                elif action_type == 'process_optimization':
                    result = self._optimize_processes()
                elif action_type == 'cache_cleanup':
                    result = self._cleanup_cache()
                    self.last_cleanup['cache'] = current_time
                elif action_type == 'temp_file_cleanup':
                    result = self._cleanup_temp_files()
                    self.last_cleanup['temp_files'] = current_time
                else:
                    result = {'status': 'skipped', 'message': f"Unknown action type: {action_type}"}

                result.update({
                    'action_type': action_type,
                    'priority': priority,
                    'timestamp': datetime.utcnow().isoformat()
                })
                results.append(result)

                # Notify about critical actions
                if priority == 'critical':
                    self.notifier.send_alert("SELF_HEALING", f"Action taken: {action_type} - {result.get('message', 'No details')}")

            except Exception as e:
                error_result = {
                    'action_type': action_type,
                    'status': 'error',
                    'message': f"Failed to perform action: {str(e)}",
                    'priority': priority,
                    'timestamp': datetime.utcnow().isoformat()
                }
                results.append(error_result)
                self.logger.error(f"Error performing {action_type}: {e}")
                self.notifier.send_alert("SELF_HEALING_ERROR", f"Failed action: {action_type} - {str(e)}")

        return results

    def _optimize_cpu(self) -> Dict[str, Any]:
        """Optimize CPU usage by identifying and terminating resource-intensive processes"""
        try:
            # Get top CPU-consuming processes
            top_processes = self.monitor._get_top_processes(limit=10)

            # Identify non-critical processes that can be terminated
            terminated_processes = []
            for process in top_processes:
                # Skip critical system processes (this should be configurable)
                if process['name'] in ['systemd', 'init', 'kthreadd', 'ksoftirqd', 'kworker', 'python']:
                    continue

                # Skip our own processes
                if 'self_healing' in process['name'].lower() or 'monitoring' in process['name'].lower():
                    continue

                try:
                    # Try to terminate the process
                    proc = psutil.Process(process['pid'])
                    proc.terminate()
                    terminated_processes.append(process)
                    self.logger.info(f"Terminated process {process['pid']} ({process['name']})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if terminated_processes:
                return {
                    'status': 'success',
                    'message': f"Terminated {len(terminated_processes)} CPU-intensive processes",
                    'details': terminated_processes
                }
            else:
                return {
                    'status': 'no_action',
                    'message': "No non-critical CPU-intensive processes found to terminate"
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to optimize CPU: {str(e)}"
            }

    def _optimize_memory(self) -> Dict[str, Any]:
        """Optimize memory usage by clearing caches and restarting memory-intensive services"""
        try:
            # Try to clear system caches (Linux-specific)
            if sys.platform == 'linux':
                try:
                    subprocess.run(['sync'], check=True)
                    with open('/proc/sys/vm/drop_caches', 'w') as f:
                        f.write('3\n')
                    return {
                        'status': 'success',
                        'message': "Cleared system caches"
                    }
                except Exception as e:
                    self.logger.warning(f"Failed to clear system caches: {e}")

            # Fallback: Try to identify and restart memory-intensive processes
            top_processes = self.monitor._get_top_processes(limit=5)
            memory_intensive = [p for p in top_processes if p['memory_percent'] > 10]

            if memory_intensive:
                # For now, just log the processes (in a real system, we'd restart them)
                return {
                    'status': 'warning',
                    'message': f"Found {len(memory_intensive)} memory-intensive processes",
                    'details': memory_intensive
                }
            else:
                return {
                    'status': 'no_action',
                    'message': "No memory-intensive processes found"
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to optimize memory: {str(e)}"
            }

    def _optimize_disk(self) -> Dict[str, Any]:
        """Optimize disk usage by cleaning up temporary files and logs"""
        try:
            # Clean up system temporary files
            temp_dirs = ['/tmp', '/var/tmp']

            total_freed = 0
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                file_stat = os.stat(file_path)
                                # Delete files older than 7 days
                                if (current_time - file_stat.st_mtime) > (7 * 86400):
                                    os.remove(file_path)
                                    total_freed += file_stat.st_size
                            except (OSError, PermissionError):
                                continue

            # Clean up old log files
            log_dirs = ['/var/log']
            for log_dir in log_dirs:
                if os.path.exists(log_dir):
                    for root, dirs, files in os.walk(log_dir):
                        for file in files:
                            if file.endswith('.log') or file.endswith('.log.1'):
                                try:
                                    file_path = os.path.join(root, file)
                                    file_stat = os.stat(file_path)
                                    # Delete log files older than 30 days
                                    if (current_time - file_stat.st_mtime) > (30 * 86400):
                                        os.remove(file_path)
                                        total_freed += file_stat.st_size
                                except (OSError, PermissionError):
                                    continue

            if total_freed > 0:
                return {
                    'status': 'success',
                    'message': f"Freed {total_freed / (1024*1024):.2f} MB of disk space"
                }
            else:
                return {
                    'status': 'no_action',
                    'message': "No old temporary files or logs found to delete"
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to optimize disk: {str(e)}"
            }

    def _optimize_processes(self) -> Dict[str, Any]:
        """Optimize process count by identifying and terminating zombie/defunct processes"""
        try:
            terminated_count = 0
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                try:
                    if proc.info['status'] in [psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
                        proc.terminate()
                        terminated_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if terminated_count > 0:
                return {
                    'status': 'success',
                    'message': f"Terminated {terminated_count} zombie/defunct processes"
                }
            else:
                return {
                    'status': 'no_action',
                    'message': "No zombie/defunct processes found"
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to optimize processes: {str(e)}"
            }

    def _cleanup_cache(self) -> Dict[str, Any]:
        """Clean up application caches"""
        try:
            # This would be application-specific in a real implementation
            # For now, we'll just simulate cache cleanup
            cache_dirs = ['/tmp/app_cache', '/var/cache/app']

            total_freed = 0
            for cache_dir in cache_dirs:
                if os.path.exists(cache_dir):
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                file_stat = os.stat(file_path)
                                os.remove(file_path)
                                total_freed += file_stat.st_size
                            except (OSError, PermissionError):
                                continue

            return {
                'status': 'success',
                'message': f"Cache cleanup completed, freed {total_freed / (1024*1024):.2f} MB"
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to cleanup cache: {str(e)}"
            }

    def _cleanup_temp_files(self) -> Dict[str, Any]:
        """Clean up temporary files"""
        try:
            # Clean up application-specific temporary files
            temp_dirs = ['/tmp/app_temp', '/var/tmp/app_temp']

            total_freed = 0
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                file_stat = os.stat(file_path)
                                os.remove(file_path)
                                total_freed += file_stat.st_size
                            except (OSError, PermissionError):
                                continue

            return {
                'status': 'success',
                'message': f"Temp file cleanup completed, freed {total_freed / (1024*1024):.2f} MB"
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to cleanup temp files: {str(e)}"
            }

    def restart_service(self, service_name: str) -> Dict[str, Any]:
        """Restart a specific service"""
        try:
            # This would use systemd or similar service manager in a real implementation
            # For now, we'll simulate service restart
            self.logger.info(f"Restarting service: {service_name}")

            # Check if the service is running first
            service_status = self.monitor.check_specific_process(service_name)
            if service_status['status'] == 'running':
                # Simulate service restart
                time.sleep(2)  # Simulate restart delay
                return {
                    'status': 'success',
                    'message': f"Service {service_name} restarted successfully"
                }
            else:
                return {
                    'status': 'warning',
                    'message': f"Service {service_name} not running, attempting to start"
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to restart service {service_name}: {str(e)}"
            }

    def trigger_failover(self, service_name: str) -> Dict[str, Any]:
        """Trigger failover for a critical service"""
        try:
            # This would implement actual failover logic in a real system
            # For now, we'll simulate failover
            self.logger.info(f"Triggering failover for service: {service_name}")

            # Simulate failover process
            time.sleep(3)  # Simulate failover delay

            return {
                'status': 'success',
                'message': f"Failover completed for service {service_name}",
                'details': {
                    'new_primary': f"{service_name}_replica_1",
                    'old_primary': f"{service_name}_primary"
                }
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to trigger failover for {service_name}: {str(e)}"
            }

    def auto_scale_resources(self, resource_type: str, amount: int) -> Dict[str, Any]:
        """Automatically scale resources up or down"""
        try:
            # This would integrate with cloud provider APIs in a real implementation
            # For now, we'll simulate resource scaling
            self.logger.info(f"Scaling {resource_type} by {amount}")

            if resource_type == 'cpu':
                # Simulate CPU scaling
                time.sleep(1)
                return {
                    'status': 'success',
                    'message': f"Scaled CPU by {amount} cores"
                }
            elif resource_type == 'memory':
                # Simulate memory scaling
                time.sleep(1)
                return {
                    'status': 'success',
                    'message': f"Scaled memory by {amount} GB"
                }
            elif resource_type == 'disk':
                # Simulate disk scaling
                time.sleep(2)
                return {
                    'status': 'success',
                    'message': f"Scaled disk by {amount} GB"
                }
            else:
                return {
                    'status': 'error',
                    'message': f"Unknown resource type: {resource_type}"
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to scale {resource_type}: {str(e)}"
            }

    def send_confirmation(self, message: str, channel: str = 'email') -> Dict[str, Any]:
        """Send confirmation about self-healing actions"""
        try:
            if channel == 'email':
                # Simulate sending email
                self.logger.info(f"Sending email confirmation: {message}")
                self.notifier.send_info("admin", f"Self-healing confirmation: {message}")
            elif channel == 'slack':
                # Simulate sending Slack message
                self.logger.info(f"Sending Slack confirmation: {message}")
                self.notifier.send_alert("SLACK", f"Self-healing: {message}")
            else:
                # Default to alert
                self.notifier.send_alert("SELF_HEALING", message)

            return {
                'status': 'success',
                'message': f"Confirmation sent via {channel}"
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f"Failed to send confirmation: {str(e)}"
            }
