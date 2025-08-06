

from clickhouse_connect.driver import Client
from logger import get_logger

class ClickHouseLogger:
    def __init__(self, host='localhost', port=8123, database='default'):
        """Initialize ClickHouse client."""
        self.client = Client(host=host, port=port, database=database)
        self.logger = get_logger()
        self._create_logs_table()

    def _create_logs_table(self):
        """Create logs table if it doesn't exist."""
        try:
            self.client.command('''
                CREATE TABLE IF NOT EXISTS logs (
                    timestamp DateTime DEFAULT now(),
                    level String,
                    message String,
                    error_code Nullable(String)
                ) ENGINE = MergeTree()
                ORDER BY timestamp
            ''')
        except Exception as e:
            self.logger.error(f"Failed to create logs table in ClickHouse: {e}")

    def log_to_clickhouse(self, level, message, error_code=None):
        """Log a message to ClickHouse."""
        try:
            # Convert to list of tuples for clickhouse-connect
            data = [(level, message, error_code)]
            self.client.insert('logs', data, column_names=['level', 'message', 'error_code'])
        except Exception as e:
            self.logger.error(f"Error writing log to ClickHouse: {e}")

def setup_clickhouse_logger(host='localhost', port=8123, database='default'):
    """Set up and return a ClickHouse logger instance."""
    return ClickHouseLogger(host, port, database)

