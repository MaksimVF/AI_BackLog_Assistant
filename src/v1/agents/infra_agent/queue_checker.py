



import redis
from typing import Dict, Any, Optional
from .base_infra_agent import BaseInfraAgent

class QueueCheckerAgent(BaseInfraAgent):
    """Agent to check Redis queue status."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        super().__init__(
            name="QueueChecker",
            config={
                "host": config.get("host", "localhost"),
                "port": config.get("port", 6379),
                "password": config.get("password"),
                "db": config.get("db", 0),
                "queue_names": config.get("queue_names", ["default", "high_priority"])
            }
        )
        self.redis_client = None
        self._connect()

    def _connect(self) -> None:
        """Establish connection to Redis."""
        try:
            self.redis_client = redis.Redis(
                host=self.config["host"],
                port=self.config["port"],
                password=self.config.get("password"),
                db=self.config["db"],
                socket_timeout=5
            )
            # Test the connection
            self.redis_client.ping()
        except redis.ConnectionError as e:
            self.redis_client = None
            raise Exception(f"Failed to connect to Redis: {e}")

    def check_status(self) -> Dict[str, Any]:
        """Check Redis queue status."""
        if not self.redis_client:
            try:
                self._connect()
            except Exception as e:
                return {
                    "status": "disconnected",
                    "error": str(e),
                    "config": {
                        "host": self.config["host"],
                        "port": self.config["port"]
                    }
                }

        try:
            # Get queue lengths
            queue_status = {}
            for queue_name in self.config["queue_names"]:
                queue_length = self.redis_client.llen(queue_name)
                queue_status[queue_name] = {
                    "length": queue_length,
                    "status": "normal" if queue_length < 1000 else "high_load"
                }

            # Get Redis info
            redis_info = self.redis_client.info()
            memory_usage = redis_info.get("used_memory_human", "unknown")

            return {
                "status": "healthy",
                "queues": queue_status,
                "memory_usage": memory_usage,
                "redis_version": redis_info.get("redis_version", "unknown")
            }
        except redis.RedisError as e:
            return {
                "status": "error",
                "error": str(e),
                "config": {
                    "host": self.config["host"],
                    "port": self.config["port"]
                }
            }

    def get_queue_length(self, queue_name: str) -> Dict[str, Any]:
        """Get length of a specific queue."""
        if not self.redis_client:
            return {"status": "disconnected", "queue": queue_name}

        try:
            length = self.redis_client.llen(queue_name)
            return {
                "status": "success",
                "queue": queue_name,
                "length": length
            }
        except redis.RedisError as e:
            return {
                "status": "error",
                "queue": queue_name,
                "error": str(e)
            }



