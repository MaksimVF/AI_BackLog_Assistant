



import os
import yaml
import logging
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any

class SelfHealingConfig(BaseModel):
    """Configuration model for SelfHealingAgent with validation"""

    cpu_critical: float = Field(95.0, ge=0, le=100)
    memory_critical: float = Field(95.0, ge=0, le=100)
    disk_critical: float = Field(90.0, ge=0, le=100)
    process_count_max: int = Field(1000, gt=0)
    cache_cleanup_interval: int = Field(86400, gt=0)  # 24 hours
    temp_file_cleanup_interval: int = Field(43200, gt=0)  # 12 hours

    @field_validator('cpu_critical', 'memory_critical', 'disk_critical')
    def check_thresholds(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Threshold must be between 0 and 100')
        return v

    @field_validator('cache_cleanup_interval', 'temp_file_cleanup_interval')
    def check_intervals(cls, v):
        if v <= 0:
            raise ValueError('Interval must be positive')
        return v

class ConfigManager:
    """Manages configuration for SelfHealingAgent with dynamic updates and environment support"""

    def __init__(self, initial_config: Optional[Dict[str, Any]] = None):
        self.logger = logging.getLogger("ConfigManager")
        self.config = SelfHealingConfig(**initial_config) if initial_config else SelfHealingConfig()
        self.environment = os.getenv('ENV', 'dev')
        self.config_sources = []

        # Load environment-specific configuration
        self.load_environment_config()

    def load_environment_config(self):
        """Load configuration based on environment"""
        config_file = f'config.{self.environment}.yaml'
        if os.path.exists(config_file):
            try:
                with open(config_file) as f:
                    env_config = yaml.safe_load(f) or {}
                    self.update_config(env_config)
                    self.config_sources.append(f"file://{config_file}")
                    self.logger.info(f"Loaded environment config from {config_file}")
            except Exception as e:
                self.logger.error(f"Failed to load environment config: {e}")
        else:
            self.logger.warning(f"No environment config file found: {config_file}")

    def update_config(self, new_config: Dict[str, Any]):
        """Update configuration with validation and logging"""
        try:
            old_config = self.config.dict()
            self.config = SelfHealingConfig(**{**old_config, **new_config})
            self.log_config_changes(old_config, self.config.dict())
            return True
        except Exception as e:
            self.logger.error(f"Failed to update config: {e}")
            return False

    def log_config_changes(self, old_config: Dict[str, Any], new_config: Dict[str, Any]):
        """Log configuration changes for audit"""
        for key in old_config.keys():
            if key in new_config and new_config[key] != old_config[key]:
                self.logger.info(f"Config change: {key} = {old_config[key]} -> {new_config[key]}")

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration as dictionary"""
        return self.config.dict()

    def load_from_file(self, file_path: str) -> bool:
        """Load configuration from a specific file"""
        try:
            with open(file_path) as f:
                file_config = yaml.safe_load(f) or {}
                if self.update_config(file_config):
                    self.config_sources.append(f"file://{file_path}")
                    self.logger.info(f"Loaded config from {file_path}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to load config from {file_path}: {e}")
            return False

    def load_from_consul(self, consul_url: str, config_path: str) -> bool:
        """Load configuration from Consul (mock implementation)"""
        # In a real implementation, this would use the consul API
        self.logger.warning("Consul integration not implemented - using mock")
        self.config_sources.append(f"consul://{consul_url}/{config_path}")
        return True

    def load_from_etcd(self, etcd_url: str, config_path: str) -> bool:
        """Load configuration from etcd (mock implementation)"""
        # In a real implementation, this would use the etcd API
        self.logger.warning("etcd integration not implemented - using mock")
        self.config_sources.append(f"etcd://{etcd_url}/{config_path}")
        return True

    def get_config_sources(self) -> list:
        """Get list of configuration sources"""
        return self.config_sources.copy()

    def watch_config_changes(self, callback):
        """Watch for configuration changes (mock implementation)"""
        # In a real implementation, this would use file watching or API polling
        self.logger.warning("Config watching not implemented - using mock")
        return lambda: None  # Return mock unsubscribe function



