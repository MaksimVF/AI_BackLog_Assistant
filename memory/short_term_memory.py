


"""
Short-term Memory Module

Uses Redis for fast, temporary storage of:
- Session data
- Recent interactions
- Temporary state information
"""

import redis
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from config import settings

class ShortTermMemory:
    """Redis-based short-term memory for session and temporary data."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 1, password: Optional[str] = None):
        """
        Initialize short-term memory with Redis connection.

        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password (if any)
        """
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            socket_timeout=5
        )

        # Test the connection
        try:
            self.redis_client.ping()
        except redis.ConnectionError as e:
            raise Exception(f"Failed to connect to Redis: {e}")

    def store_session(self, session_id: str, data: Dict[str, Any], ttl: int = 3600) -> bool:
        """
        Store session data with optional time-to-live.

        Args:
            session_id: Unique session identifier
            data: Session data to store
            ttl: Time-to-live in seconds (default: 1 hour)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add timestamp
            data_with_meta = {
                "data": data,
                "created_at": datetime.now().isoformat(),
                "ttl": ttl
            }
            self.redis_client.setex(f"session:{session_id}", ttl, json.dumps(data_with_meta))
            return True
        except Exception as e:
            print(f"Error storing session {session_id}: {e}")
            return False

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data.

        Args:
            session_id: Unique session identifier

        Returns:
            Session data if found, None otherwise
        """
        try:
            data = self.redis_client.get(f"session:{session_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error retrieving session {session_id}: {e}")
            return None

    def store_interaction(self, interaction_id: str, data: Dict[str, Any], ttl: int = 86400) -> bool:
        """
        Store user interaction data.

        Args:
            interaction_id: Unique interaction identifier
            data: Interaction data to store
            ttl: Time-to-live in seconds (default: 24 hours)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data_with_meta = {
                "data": data,
                "created_at": datetime.now().isoformat(),
                "ttl": ttl
            }
            self.redis_client.setex(f"interaction:{interaction_id}", ttl, json.dumps(data_with_meta))
            return True
        except Exception as e:
            print(f"Error storing interaction {interaction_id}: {e}")
            return False

    def get_interaction(self, interaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve interaction data.

        Args:
            interaction_id: Unique interaction identifier

        Returns:
            Interaction data if found, None otherwise
        """
        try:
            data = self.redis_client.get(f"interaction:{interaction_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error retrieving interaction {interaction_id}: {e}")
            return None

    def store_state(self, state_key: str, state_data: Dict[str, Any], ttl: int = 7200) -> bool:
        """
        Store temporary state information.

        Args:
            state_key: Unique state key
            state_data: State data to store
            ttl: Time-to-live in seconds (default: 2 hours)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            state_with_meta = {
                "data": state_data,
                "created_at": datetime.now().isoformat(),
                "ttl": ttl
            }
            self.redis_client.setex(f"state:{state_key}", ttl, json.dumps(state_with_meta))
            return True
        except Exception as e:
            print(f"Error storing state {state_key}: {e}")
            return False

    def get_state(self, state_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve state data.

        Args:
            state_key: Unique state key

        Returns:
            State data if found, None otherwise
        """
        try:
            data = self.redis_client.get(f"state:{state_key}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error retrieving state {state_key}: {e}")
            return None

    def delete_key(self, key: str) -> bool:
        """
        Delete a key from short-term memory.

        Args:
            key: Key to delete

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return self.redis_client.delete(key) > 0
        except Exception as e:
            print(f"Error deleting key {key}: {e}")
            return False

    def clear_expired(self) -> int:
        """
        Clear expired keys (Redis handles this automatically, but we can implement custom logic).

        Returns:
            Number of keys cleared
        """
        # Redis automatically handles key expiration
        # This method is a placeholder for any custom cleanup logic
        return 0

    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory usage statistics.

        Returns:
            Dictionary with memory statistics
        """
        try:
            info = self.redis_client.info("memory")
            return {
                "used_memory": info.get("used_memory", "unknown"),
                "used_memory_human": info.get("used_memory_human", "unknown"),
                "used_memory_rss": info.get("used_memory_rss", "unknown"),
                "used_memory_peak": info.get("used_memory_peak", "unknown"),
                "memory_fragmentation_ratio": info.get("mem_fragmentation_ratio", "unknown")
            }
        except Exception as e:
            print(f"Error getting memory stats: {e}")
            return {}

    def get_all_keys(self, pattern: str = "*") -> List[str]:
        """
        Get all keys matching a pattern.

        Args:
            pattern: Pattern to match (default: all keys)

        Returns:
            List of matching keys
        """
        try:
            return [key.decode() for key in self.redis_client.keys(pattern)]
        except Exception as e:
            print(f"Error getting keys: {e}")
            return []

    @classmethod
    def from_config(cls):
        """Create ShortTermMemory instance from configuration."""
        from urllib.parse import urlparse

        # Parse Redis URL
        redis_url = urlparse(settings.REDIS_URL)
        host = redis_url.hostname or "localhost"
        port = redis_url.port or 6379

        return cls(
            host=host,
            port=port,
            db=1,  # Use database 1 for short-term memory
            password=None  # Add password support if needed
        )


