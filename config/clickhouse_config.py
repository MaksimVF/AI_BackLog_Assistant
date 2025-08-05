


"""
ClickHouse configuration
"""

import os
from typing import Dict, Any

def get_clickhouse_config() -> Dict[str, Any]:
    """Get ClickHouse and Kafka configuration from environment variables"""
    return {
        # ClickHouse configuration
        'clickhouse_host': os.getenv('CLICKHOUSE_HOST', 'localhost'),
        'clickhouse_port': int(os.getenv('CLICKHOUSE_PORT', 8443)),
        'clickhouse_username': os.getenv('CLICKHOUSE_USER', 'default'),
        'clickhouse_password': os.getenv('CLICKHOUSE_PASSWORD', ''),
        'clickhouse_database': os.getenv('CLICKHOUSE_DATABASE', 'ai_backlog_admin'),
        'clickhouse_secure': os.getenv('CLICKHOUSE_SECURE', 'true').lower() == 'true',
        'clickhouse_verify': os.getenv('CLICKHOUSE_VERIFY', 'true').lower() == 'true',
        'clickhouse_ca_cert': os.getenv('CLICKHOUSE_CA_CERT', None),

        # Kafka configuration
        'kafka_servers': os.getenv('KAFKA_SERVERS', 'localhost:9092'),
        'kafka_client_id': os.getenv('KAFKA_CLIENT_ID', 'ai-backlog-agent'),
        'kafka_security_protocol': os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
        'kafka_sasl_mechanisms': os.getenv('KAFKA_SASL_MECHANISMS', ''),
        'kafka_sasl_username': os.getenv('KAFKA_SASL_USERNAME', ''),
        'kafka_sasl_password': os.getenv('KAFKA_SASL_PASSWORD', ''),
    }

