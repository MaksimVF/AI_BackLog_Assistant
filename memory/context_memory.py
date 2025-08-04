



"""
Context Memory Module

Enhanced context memory with:
- Redis persistence
- Semantic search capabilities
- Context management for agents
"""

import redis
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Optional import for semantic search
try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMER_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMER_AVAILABLE = False
    print("Warning: sentence_transformers not available. Semantic search will use fallback keyword matching.")

from config import settings

class ContextMemory:
    """
    Enhanced ContextMemoryAgent with Redis persistence and semantic search.

    Features:
    - Context storage and retrieval
    - Semantic similarity search
    - Redis persistence
    - Context management
    """

    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, redis_db: int = 2, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize ContextMemory with Redis and semantic model.

        Args:
            redis_host: Redis host
            redis_port: Redis port
            redis_db: Redis database number
            model_name: SentenceTransformer model name
        """
        # Initialize Redis client
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True,
            socket_timeout=5
        )

        # Test Redis connection
        try:
            self.redis_client.ping()
        except redis.ConnectionError as e:
            raise Exception(f"Failed to connect to Redis: {e}")

        # Initialize semantic model
        if SENTENCE_TRANSFORMER_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception as e:
                print(f"Warning: Could not load SentenceTransformer model: {e}")
                self.model = None
        else:
            self.model = None

    def add_context(self, context_id: str, context: Dict[str, Any], ttl: int = 2592000) -> bool:
        """
        Add context to memory with Redis persistence.

        Args:
            context_id: Unique context identifier
            context: Context data (must include 'text')
            ttl: Time-to-live in seconds (default: 30 days)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add metadata
            context_with_meta = {
                "context_id": context_id,
                "data": context,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            # Add embedding if model is available
            if self.model and "text" in context:
                embedding = self.model.encode(context["text"], convert_to_tensor=True)
                context_with_meta["embedding"] = embedding.tolist()

            # Store in Redis
            self.redis_client.setex(f"context:{context_id}", ttl, json.dumps(context_with_meta))
            return True
        except Exception as e:
            print(f"Error adding context {context_id}: {e}")
            return False

    def get_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve context by ID.

        Args:
            context_id: Unique context identifier

        Returns:
            Context data if found, None otherwise
        """
        try:
            data = self.redis_client.get(f"context:{context_id}")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error retrieving context {context_id}: {e}")
            return None

    def retrieve_relevant(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve top_k most relevant contexts using semantic search.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant contexts
        """
        if not self.model:
            # Fallback to keyword search if semantic model not available
            return self._keyword_search(query, top_k)

        try:
            # Get query embedding
            query_emb = self.model.encode(query, convert_to_tensor=True)

            # Get all contexts
            context_keys = self.redis_client.keys("context:*")
            scored_contexts = []

            for key in context_keys:
                context_data = self.redis_client.get(key)
                if context_data:
                    context = json.loads(context_data)
                    if "embedding" in context:
                        # Convert embedding back to tensor
                        embedding = self.model.encode(context["data"].get("text", ""), convert_to_tensor=True)
                        sim = util.pytorch_cos_sim(query_emb, embedding)[0][0].item()
                        scored_contexts.append((sim, context))

            # Sort by similarity
            scored_contexts.sort(reverse=True, key=lambda x: x[0])

            # Return top_k results
            return [context for _, context in scored_contexts[:top_k]]

        except Exception as e:
            print(f"Error in semantic search: {e}")
            return self._keyword_search(query, top_k)

    def _keyword_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Fallback keyword search when semantic model is unavailable.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant contexts
        """
        try:
            query_words = set(query.lower().split())
            context_keys = self.redis_client.keys("context:*")
            scored = []

            for key in context_keys:
                context_data = self.redis_client.get(key)
                if context_data:
                    context = json.loads(context_data)
                    text = context["data"].get("text", "").lower()
                    common_words = len(query_words.intersection(text.split()))
                    score = common_words / max(len(query_words), 1)
                    scored.append((score, context))

            scored.sort(reverse=True, key=lambda x: x[0])
            return [context for _, context in scored[:top_k]]
        except Exception as e:
            print(f"Error in keyword search: {e}")
            return []

    def update_context(self, context_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update existing context.

        Args:
            context_id: Unique context identifier
            updates: Dictionary of updates

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            context_data = self.redis_client.get(f"context:{context_id}")
            if not context_data:
                return False

            context = json.loads(context_data)
            context["data"].update(updates)
            context["updated_at"] = datetime.now().isoformat()

            # Update embedding if text changed
            if self.model and "text" in updates:
                embedding = self.model.encode(context["data"]["text"], convert_to_tensor=True)
                context["embedding"] = embedding.tolist()

            self.redis_client.setex(f"context:{context_id}", 2592000, json.dumps(context))
            return True
        except Exception as e:
            print(f"Error updating context {context_id}: {e}")
            return False

    def delete_context(self, context_id: str) -> bool:
        """
        Delete context from memory.

        Args:
            context_id: Unique context identifier

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return self.redis_client.delete(f"context:{context_id}") > 0
        except Exception as e:
            print(f"Error deleting context {context_id}: {e}")
            return False

    def get_all_contexts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all contexts (limited for performance).

        Args:
            limit: Maximum number of contexts to return

        Returns:
            List of all contexts
        """
        try:
            context_keys = self.redis_client.keys("context:*")[:limit]
            contexts = []

            for key in context_keys:
                context_data = self.redis_client.get(key)
                if context_data:
                    contexts.append(json.loads(context_data))

            return contexts
        except Exception as e:
            print(f"Error getting all contexts: {e}")
            return []

    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get context memory statistics.

        Returns:
            Dictionary with memory statistics
        """
        try:
            context_count = len(self.redis_client.keys("context:*"))
            info = self.redis_client.info("memory")

            return {
                "context_count": context_count,
                "used_memory": info.get("used_memory", "unknown"),
                "used_memory_human": info.get("used_memory_human", "unknown")
            }
        except Exception as e:
            print(f"Error getting memory stats: {e}")
            return {}

    def clear_memory(self) -> int:
        """
        Clear all contexts from memory.

        Returns:
            Number of contexts cleared
        """
        try:
            context_keys = self.redis_client.keys("context:*")
            if context_keys:
                self.redis_client.delete(*context_keys)
            return len(context_keys)
        except Exception as e:
            print(f"Error clearing memory: {e}")
            return 0

    @classmethod
    def from_config(cls):
        """Create ContextMemory instance from configuration."""
        from urllib.parse import urlparse

        # Parse Redis URL
        redis_url = urlparse(settings.REDIS_URL)
        host = redis_url.hostname or "localhost"
        port = redis_url.port or 6379

        return cls(
            redis_host=host,
            redis_port=port,
            redis_db=2,  # Use database 2 for context memory
            model_name=settings.EMBEDDING_MODEL_NAME
        )



