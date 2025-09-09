



import os
import sys
import json
import logging
import logging.handlers
from datetime import datetime
from typing import Optional, Dict, Any, Union, List
from logging import Logger, LogRecord

class EnhancedJSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def __init__(self, service_name: str = "AI_BackLog_Assistant", environment: str = "dev"):
        super().__init__()
        self.service_name = service_name
        self.environment = environment

    def format(self, record: LogRecord) -> str:
        """Format log record as JSON"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'service': self.service_name,
            'environment': self.environment,
            'message': record.getMessage(),
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        # Add any custom attributes from the record
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'exc_info', 'funcName', 'lineno',
                          'created', 'msecs', 'relativeCreated', 'thread', 'threadName',
                          'processName', 'process', 'message']:
                log_entry[key] = value

        return json.dumps(log_entry, ensure_ascii=False)

class LoggingManager:
    """Advanced logging manager with rotation, archiving, and external integration"""

    def __init__(self,
                 service_name: str = "AI_BackLog_Assistant",
                 environment: str = "dev",
                 log_level: str = "INFO",
                 log_file: str = "app.log",
                 max_bytes: int = 10485760,  # 10MB
                 backup_count: int = 5,
                 use_console: bool = True,
                 use_file: bool = True,
                 external_systems: Optional[Dict[str, Any]] = None):
        """
        Initialize logging manager with advanced configuration

        Args:
            service_name: Name of the service
            environment: Environment (dev/test/prod)
            log_level: Minimum log level
            log_file: Log file path
            max_bytes: Maximum log file size before rotation
            backup_count: Number of backup files to keep
            use_console: Enable console logging
            use_file: Enable file logging
            external_systems: Configuration for external logging systems
        """
        self.service_name = service_name
        self.environment = environment
        self.log_level = log_level
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.use_console = use_console
        self.use_file = use_file
        self.external_systems = external_systems or {}
        self.loggers = {}
        self._configure_logging()

    def _configure_logging(self):
        """Configure logging with handlers and formatters"""
        # Set up the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)

        # Clear any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Create JSON formatter
        formatter = EnhancedJSONFormatter(
            service_name=self.service_name,
            environment=self.environment
        )

        # Add console handler if enabled
        if self.use_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        # Add file handler with rotation if enabled
        if self.use_file:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_bytes,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        # Configure external logging systems
        self._configure_external_logging()

    def _configure_external_logging(self):
        """Configure external logging systems like ELK, Splunk, etc."""
        if 'elk' in self.external_systems:
            self._configure_elk_logging(self.external_systems['elk'])

        if 'splunk' in self.external_systems:
            self._configure_splunk_logging(self.external_systems['splunk'])

        if 'http' in self.external_systems:
            self._configure_http_logging(self.external_systems['http'])

    def _configure_elk_logging(self, elk_config: Dict[str, Any]):
        """Configure ELK (Elasticsearch) logging"""
        try:
            from elasticsearch import Elasticsearch
            from elasticsearch.helpers import BulkIndexError

            elk_handler = logging.StreamHandler()
            elk_handler.setLevel(self.log_level)
            elk_handler.setFormatter(EnhancedJSONFormatter(
                service_name=self.service_name,
                environment=self.environment
            ))

            # Create ELK client
            elk_client = Elasticsearch(
                hosts=[elk_config.get('host', 'localhost:9200')],
                http_auth=(elk_config.get('username'), elk_config.get('password'))
            )

            def elk_emit(record):
                """Send log record to ELK"""
                try:
                    log_entry = json.loads(elk_handler.format(record))
                    elk_client.index(
                        index=elk_config.get('index', 'logs'),
                        document=log_entry
                    )
                except (BulkIndexError, ConnectionError) as e:
                    # Fallback to regular logging if ELK fails
                    logging.getLogger('elk_fallback').error(f"ELK logging failed: {e}")

            elk_handler.emit = elk_emit
            logging.getLogger().addHandler(elk_handler)
            logging.getLogger('elk').info("ELK logging configured successfully")

        except ImportError:
            logging.getLogger('elk').warning("Elasticsearch not installed, ELK logging disabled")
        except Exception as e:
            logging.getLogger('elk').error(f"Failed to configure ELK logging: {e}")

    def _configure_splunk_logging(self, splunk_config: Dict[str, Any]):
        """Configure Splunk logging"""
        try:
            import splunklib.client as client
            import splunklib.data as data

            splunk_handler = logging.StreamHandler()
            splunk_handler.setLevel(self.log_level)
            splunk_handler.setFormatter(EnhancedJSONFormatter(
                service_name=self.service_name,
                environment=self.environment
            ))

            # Create Splunk client
            splunk_service = client.connect(
                host=splunk_config.get('host', 'localhost'),
                port=splunk_config.get('port', 8089),
                username=splunk_config.get('username'),
                password=splunk_config.get('password')
            )

            def splunk_emit(record):
                """Send log record to Splunk"""
                try:
                    log_entry = json.loads(splunk_handler.format(record))
                    event = data.Event(
                        data=json.dumps(log_entry),
                        sourcetype=splunk_config.get('sourcetype', '_json'),
                        index=splunk_config.get('index', 'main'),
                        host=self.service_name
                    )
                    splunk_service.events.write(event)
                except Exception as e:
                    # Fallback to regular logging if Splunk fails
                    logging.getLogger('splunk_fallback').error(f"Splunk logging failed: {e}")

            splunk_handler.emit = splunk_emit
            logging.getLogger().addHandler(splunk_handler)
            logging.getLogger('splunk').info("Splunk logging configured successfully")

        except ImportError:
            logging.getLogger('splunk').warning("Splunk library not installed, Splunk logging disabled")
        except Exception as e:
            logging.getLogger('splunk').error(f"Failed to configure Splunk logging: {e}")

    def _configure_http_logging(self, http_config: Dict[str, Any]):
        """Configure HTTP logging"""
        try:
            import requests

            http_handler = logging.StreamHandler()
            http_handler.setLevel(self.log_level)
            http_handler.setFormatter(EnhancedJSONFormatter(
                service_name=self.service_name,
                environment=self.environment
            ))

            def http_emit(record):
                """Send log record via HTTP"""
                try:
                    log_entry = json.loads(http_handler.format(record))
                    headers = http_config.get('headers', {'Content-Type': 'application/json'})
                    auth = None

                    if 'username' in http_config and 'password' in http_config:
                        auth = (http_config['username'], http_config['password'])

                    response = requests.post(
                        http_config['url'],
                        json=log_entry,
                        headers=headers,
                        auth=auth,
                        timeout=http_config.get('timeout', 5)
                    )

                    if not response.ok:
                        logging.getLogger('http_fallback').error(
                            f"HTTP logging failed: {response.status_code} - {response.text}"
                        )

                except Exception as e:
                    # Fallback to regular logging if HTTP fails
                    logging.getLogger('http_fallback').error(f"HTTP logging failed: {e}")

            http_handler.emit = http_emit
            logging.getLogger().addHandler(http_handler)
            logging.getLogger('http').info("HTTP logging configured successfully")

        except ImportError:
            logging.getLogger('http').warning("Requests library not installed, HTTP logging disabled")
        except Exception as e:
            logging.getLogger('http').error(f"Failed to configure HTTP logging: {e}")

    def get_logger(self, name: Optional[str] = None) -> Logger:
        """Get a logger with the specified name"""
        if name is None:
            return logging.getLogger(self.service_name)
        return logging.getLogger(f"{self.service_name}.{name}")

    def set_log_level(self, level: str):
        """Dynamically change the log level"""
        self.log_level = level
        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        for handler in root_logger.handlers:
            handler.setLevel(level)

    def add_context(self, **context):
        """Add context information to all subsequent log messages"""
        # This would be implemented using a ThreadLocal or similar approach
        # For simplicity, we'll use a logger adapter
        logger = logging.getLogger()
        return logging.LoggerAdapter(logger, context)

    def archive_logs(self, archive_dir: str = "log_archive") -> List[str]:
        """Archive and compress old log files"""
        import glob
        import shutil
        import gzip

        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)

        archived_files = []
        log_pattern = f"{self.log_file}.*"  # Match rotated log files

        for log_file in glob.glob(log_pattern):
            try:
                # Compress the log file
                archive_path = os.path.join(archive_dir, f"{os.path.basename(log_file)}.gz")
                with open(log_file, 'rb') as f_in:
                    with gzip.open(archive_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Remove the original file
                os.remove(log_file)
                archived_files.append(archive_path)

            except Exception as e:
                logging.getLogger('archive').error(f"Failed to archive {log_file}: {e}")

        return archived_files

    def cleanup_old_logs(self, max_age_days: int = 30) -> List[str]:
        """Clean up old log files"""
        import glob
        from datetime import datetime, timedelta

        deleted_files = []
        log_pattern = f"{self.log_file}.*"  # Match rotated log files
        cutoff_time = datetime.now() - timedelta(days=max_age_days)

        for log_file in glob.glob(log_pattern):
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                if file_time < cutoff_time:
                    os.remove(log_file)
                    deleted_files.append(log_file)

            except Exception as e:
                logging.getLogger('cleanup').error(f"Failed to delete {log_file}: {e}")

        return deleted_files

    def log_exception(self, message: str, exc_info: Exception):
        """Log an exception with full traceback"""
        logger = logging.getLogger('exception')
        logger.error(message, exc_info=exc_info)

    def log_metric(self, metric_name: str, value: Union[int, float], **tags):
        """Log a metric with tags"""
        logger = logging.getLogger('metrics')
        metric_data = {
            'metric': metric_name,
            'value': value,
            'tags': tags,
            'timestamp': datetime.utcnow().isoformat()
        }
        logger.info("Metric logged", extra=metric_data)

    def log_audit(self, action: str, user: str, resource: str, status: str, **details):
        """Log an audit event"""
        logger = logging.getLogger('audit')
        audit_data = {
            'action': action,
            'user': user,
            'resource': resource,
            'status': status,
            'details': details,
            'timestamp': datetime.utcnow().isoformat()
        }
        logger.info("Audit event", extra=audit_data)

    def log_health_check(self, service: str, status: str, **metrics):
        """Log a health check result"""
        logger = logging.getLogger('health')
        health_data = {
            'service': service,
            'status': status,
            'metrics': metrics,
            'timestamp': datetime.utcnow().isoformat()
        }
        logger.info("Health check", extra=health_data)

# Initialize the logging manager
def initialize_logging(service_name: str = "AI_BackLog_Assistant",
                      environment: str = "dev",
                      log_level: str = "INFO",
                      external_systems: Optional[Dict[str, Any]] = None):
    """Initialize the logging system"""
    return LoggingManager(
        service_name=service_name,
        environment=environment,
        log_level=log_level,
        external_systems=external_systems
    )

# Create a global logging manager instance
logging_manager = initialize_logging()

# Example usage
if __name__ == "__main__":
    # Get a logger
    logger = logging_manager.get_logger()

    # Log some messages
    logger.info("This is an informational message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Log with context
    context_logger = logging_manager.add_context(user_id="12345", session_id="abcde")
    context_logger.info("User action with context")

    # Log a metric
    logging_manager.log_metric("response_time", 120.5, endpoint="/api/v1/health")

    # Log an audit event
    logging_manager.log_audit("login", "user123", "auth_service", "success")

    # Log a health check
    logging_manager.log_health_check("database", "healthy", connection_time=5, query_time=2)

    # Archive old logs
    archived = logging_manager.archive_logs()
    print(f"Archived logs: {archived}")

    # Clean up old logs
    deleted = logging_manager.cleanup_old_logs()
    print(f"Deleted logs: {deleted}")




