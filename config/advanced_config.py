


"""
Advanced configuration management with validation and reloading
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from .config_schema import ConfigSchema, load_config_from_file
from .config_watcher import ConfigFileWatcher

logger = logging.getLogger(__name__)

class AdvancedConfig:
    """
    Advanced configuration manager with validation and automatic reloading
    """

    def __init__(self, config_file: Optional[str] = None, env_file: Optional[str] = None):
        """
        Initialize configuration manager

        Args:
            config_file: Path to configuration file
            env_file: Path to environment file
        """
        self.config_file = config_file or "config.yaml"
        self.env_file = env_file or ".env"
        self._config = None
        self._watcher = None

        # Load environment variables
        if self.env_file:
            load_dotenv(dotenv_path=self.env_file)

        # Initial configuration load
        self.reload_config()

    def reload_config(self):
        """Reload configuration from file with validation"""
        try:
            # Load from file if it exists
            if os.path.exists(self.config_file):
                self._config = load_config_from_file(self.config_file)
            else:
                # Fallback to environment variables
                self._config = self._load_from_environment()
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def _load_from_environment(self) -> ConfigSchema:
        """Load configuration from environment variables"""
        config_data = {
            "clickhouse": {
                "host": os.getenv("CLICKHOUSE_HOST", "localhost"),
                "port": int(os.getenv("CLICKHOUSE_PORT", "8443")),
                "username": os.getenv("CLICKHOUSE_USER", "default"),
                "password": os.getenv("CLICKHOUSE_PASSWORD", ""),
                "database": os.getenv("CLICKHOUSE_DATABASE", "ai_backlog_admin"),
                "secure": os.getenv("CLICKHOUSE_SECURE", "true").lower() == "true",
                "ca_cert": os.getenv("CLICKHOUSE_CA_CERT")
            },
            "redis": {
                "url": os.getenv("REDIS_URL", "redis://localhost:6379/0")
            },
            "kafka": {
                "bootstrap_servers": os.getenv("KAFKA_SERVERS", "localhost:9092"),
                "client_id": os.getenv("KAFKA_CLIENT_ID", "ai-backlog-agent"),
                "security_protocol": os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT"),
                "sasl_mechanisms": os.getenv("KAFKA_SASL_MECHANISMS"),
                "sasl_username": os.getenv("KAFKA_SASL_USERNAME"),
                "sasl_password": os.getenv("KAFKA_SASL_PASSWORD")
            },
            "security": {
                "secret_key": os.getenv("SECRET_KEY", "your-secret-key-here"),
                "algorithm": os.getenv("ALGORITHM", "HS256"),
                "access_token_expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
                "allowed_ips": os.getenv("ALLOWED_IPS", "").split(",")
            },
            "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO")
        }
        return ConfigSchema(**config_data)

    def start_watching(self, debounce_seconds: float = 1.0):
        """Start watching configuration file for changes"""
        if not os.path.exists(self.config_file):
            logger.warning(f"Config file {self.config_file} does not exist, watching disabled")
            return

        self._watcher = ConfigFileWatcher(
            self.config_file,
            self.reload_config,
            debounce_seconds
        )
        self._watcher.start()

    def stop_watching(self):
        """Stop watching configuration file"""
        if self._watcher:
            self._watcher.stop()
            self._watcher = None

    @property
    def config(self) -> ConfigSchema:
        """Get current configuration"""
        if not self._config:
            self.reload_config()
        return self._config

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_watching()

# Global configuration instance
config = AdvancedConfig()

