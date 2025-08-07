
"""
Configuration schema validation using Pydantic
"""
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class DatabaseConfig(BaseModel):
    """Database configuration schema"""
    host: str = Field(..., description="Database host")
    port: int = Field(..., description="Database port")
    username: str = Field(..., description="Database username")
    password: str = Field(..., description="Database password")
    database: str = Field(..., description="Database name")
    secure: bool = Field(True, description="Use secure connection")

    @validator('port')
    def validate_port(cls, v):
        if not (1 <= v <= 65535):
            raise ValueError('Port must be between 1 and 65535')
        return v

class RedisConfig(BaseModel):
    """Redis configuration schema"""
    url: str = Field(..., description="Redis connection URL")

class ClickHouseConfig(DatabaseConfig):
    """ClickHouse specific configuration"""
    ca_cert: Optional[str] = Field(None, description="CA certificate path")

class KafkaConfig(BaseModel):
    """Kafka configuration schema"""
    bootstrap_servers: str = Field(..., description="Kafka bootstrap servers")
    client_id: str = Field("ai-backlog-agent", description="Kafka client ID")
    security_protocol: str = Field("PLAINTEXT", description="Security protocol")
    sasl_mechanisms: Optional[str] = Field(None, description="SASL mechanisms")
    sasl_username: Optional[str] = Field(None, description="SASL username")
    sasl_password: Optional[str] = Field(None, description="SASL password")

class SecurityConfig(BaseModel):
    """Security configuration schema"""
    secret_key: str = Field(..., description="Secret key for JWT")
    algorithm: str = Field("HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(30, description="Token expiration time")
    allowed_ips: List[str] = Field([], description="Allowed IP addresses")

class ConfigSchema(BaseModel):
    """Main configuration schema"""
    clickhouse: ClickHouseConfig
    redis: RedisConfig
    kafka: KafkaConfig
    security: SecurityConfig
    debug_mode: bool = Field(False, description="Enable debug mode")
    log_level: str = Field("INFO", description="Logging level")

    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Invalid log level: {v}. Must be one of: {valid_levels}')
        return v.upper()

def load_config(config_data: Dict[str, Any]) -> ConfigSchema:
    """
    Load and validate configuration data

    Args:
        config_data: Dictionary with configuration data

    Returns:
        Validated ConfigSchema instance

    Raises:
        ValidationError: If configuration is invalid
    """
    try:
        return ConfigSchema(**config_data)
    except ValidationError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise

def load_config_from_file(config_file: str) -> ConfigSchema:
    """
    Load configuration from YAML file

    Args:
        config_file: Path to configuration file

    Returns:
        Validated ConfigSchema instance
    """
    import yaml

    try:
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        return load_config(config_data)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_file}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        raise
