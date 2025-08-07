


"""
Test script for the new configuration system
"""
import logging
from config.advanced_config import AdvancedConfig, config
from config.config_schema import ConfigSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_config_validation():
    """Test configuration validation"""
    print("=== Testing Configuration Validation ===")

    # Test with valid configuration
    valid_config = {
        "clickhouse": {
            "host": "localhost",
            "port": 8443,
            "username": "default",
            "password": "",
            "database": "test_db",
            "secure": True
        },
        "redis": {
            "url": "redis://localhost:6379/0"
        },
        "kafka": {
            "bootstrap_servers": "localhost:9092",
            "client_id": "test-client"
        },
        "security": {
            "secret_key": "test-secret",
            "algorithm": "HS256",
            "access_token_expire_minutes": 30,
            "allowed_ips": ["127.0.0.1"]
        },
        "debug_mode": False,
        "log_level": "INFO"
    }

    try:
        validated = ConfigSchema(**valid_config)
        print("✅ Valid configuration passed validation")
    except Exception as e:
        print(f"❌ Valid configuration failed: {e}")

    # Test with invalid configuration
    invalid_config = {
        "clickhouse": {
            "host": "localhost",
            "port": 99999,  # Invalid port
            "username": "default",
            "password": "",
            "database": "test_db",
            "secure": True
        },
        "redis": {
            "url": "redis://localhost:6379/0"
        },
        "kafka": {
            "bootstrap_servers": "localhost:9092",
            "client_id": "test-client"
        },
        "security": {
            "secret_key": "test-secret",
            "algorithm": "HS256",
            "access_token_expire_minutes": 30,
            "allowed_ips": ["127.0.0.1"]
        },
        "debug_mode": False,
        "log_level": "INVALID"  # Invalid log level
    }

    try:
        ConfigSchema(**invalid_config)
        print("❌ Invalid configuration passed validation (should fail)")
    except Exception as e:
        print(f"✅ Invalid configuration correctly failed: {e}")

def test_config_loading():
    """Test configuration loading from file"""
    print("\n=== Testing Configuration Loading ===")

    # Test loading from environment variables
    try:
        env_config = config.config
        print("✅ Environment configuration loaded successfully")
        print(f"   - ClickHouse host: {env_config.clickhouse.host}")
        print(f"   - Redis URL: {env_config.redis.url}")
        print(f"   - Log level: {env_config.log_level}")
    except Exception as e:
        print(f"❌ Failed to load environment configuration: {e}")

def test_config_watching():
    """Test configuration file watching"""
    print("\n=== Testing Configuration Watching ===")

    # Create a temporary config file for testing
    test_config_file = "test_config.yaml"
    test_config_content = """
clickhouse:
  host: "test-host"
  port: 8443
  username: "test-user"
  password: "test-pass"
  database: "test_db"
  secure: true

redis:
  url: "redis://test-host:6379/0"

kafka:
  bootstrap_servers: "test-host:9092"
  client_id: "test-client"

security:
  secret_key: "test-secret"
  algorithm: "HS256"
  access_token_expire_minutes: 30
  allowed_ips: ["127.0.0.1"]

debug_mode: true
log_level: "DEBUG"
"""

    # Write test config file
    with open(test_config_file, 'w') as f:
        f.write(test_config_content)

    # Test config watcher
    try:
        test_config = AdvancedConfig(test_config_file)
        print("✅ Test configuration loaded successfully")
        print(f"   - Debug mode: {test_config.config.debug_mode}")
        print(f"   - Log level: {test_config.config.log_level}")

        # Test watching (briefly)
        test_config.start_watching()
        import time
        time.sleep(2)  # Let it watch for a moment
        test_config.stop_watching()
        print("✅ Configuration watching tested")

    except Exception as e:
        print(f"❌ Failed to test config watching: {e}")
    finally:
        # Clean up
        try:
            os.remove(test_config_file)
        except:
            pass

if __name__ == "__main__":
    test_config_validation()
    test_config_loading()
    test_config_watching()
    print("\n🎉 All configuration tests completed!")

