


"""
ClickHouse configuration
"""

import os
from typing import Dict, Any

def get_clickhouse_config() -> Dict[str, Any]:
    """Get ClickHouse configuration from environment variables"""
    return {
        'host': os.getenv('CLICKHOUSE_HOST', 'localhost'),
        'port': int(os.getenv('CLICKHOUSE_PORT', 8443)),
        'username': os.getenv('CLICKHOUSE_USER', 'default'),
        'password': os.getenv('CLICKHOUSE_PASSWORD', ''),
        'database': os.getenv('CLICKHOUSE_DATABASE', 'ai_backlog_admin'),
        'secure': os.getenv('CLICKHOUSE_SECURE', 'true').lower() == 'true',
        'verify': os.getenv('CLICKHOUSE_VERIFY', 'true').lower() == 'true',
        'ca_cert': os.getenv('CLICKHOUSE_CA_CERT', None),
    }

