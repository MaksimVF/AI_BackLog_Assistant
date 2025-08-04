



"""
Memory Manager

Unified interface for all memory systems:
- Short-term memory (Redis)
- Long-term memory (Weaviate)
- Context memory (Redis + semantic search)
"""

from typing import Dict, Any, Optional, List, Union
from .short_term_memory import ShortTermMemory
from .context_memory import ContextMemory
from .weaviate_client import WeaviateMemory

class MemoryManager:
    """Unified memory manager for all memory systems."""

    def __init__(self):
        """Initialize all memory systems."""
        self.short_term = ShortTermMemory.from_config()
        try:
            self.long_term = WeaviateMemory()
        except Exception as e:
            print(f"Warning: Weaviate not available: {e}")
            self.long_term = None
        self.context = ContextMemory.from_config()

    # Short-term memory methods
    def store_session(self, session_id: str, data: Dict[str, Any], ttl: int = 3600) -> bool:
        """Store session data in short-term memory."""
        return self.short_term.store_session(session_id, data, ttl)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data from short-term memory."""
        return self.short_term.get_session(session_id)

    def store_interaction(self, interaction_id: str, data: Dict[str, Any], ttl: int = 86400) -> bool:
        """Store user interaction in short-term memory."""
        return self.short_term.store_interaction(interaction_id, data, ttl)

    def get_interaction(self, interaction_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve interaction data from short-term memory."""
        return self.short_term.get_interaction(interaction_id)

    def store_state(self, state_key: str, state_data: Dict[str, Any], ttl: int = 7200) -> bool:
        """Store temporary state in short-term memory."""
        return self.short_term.store_state(state_key, state_data, ttl)

    def get_state(self, state_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve state data from short-term memory."""
        return self.short_term.get_state(state_key)

    # Long-term memory methods
    def store_case(self, case_id: str, content: str, context: str, domain_tags: List[str], metadata: Optional[Dict] = None) -> Dict:
        """Store case in long-term memory (Weaviate)."""
        return self.long_term.store_case(case_id, content, context, domain_tags, metadata)

    def update_case_status(self, case_id: str, status: str, agents: List[str]) -> Dict:
        """Update case status in long-term memory."""
        return self.long_term.update_case_status(case_id, status, agents)

    def find_similar_case(self, text: str) -> Optional[str]:
        """Find similar case in long-term memory."""
        return self.long_term.find_similar_case(text)

    def query_similar_cases(self, text: str, limit: int = 3) -> List[Dict]:
        """Query similar cases from long-term memory."""
        return self.long_term.query_similar_cases(text, limit)

    # Context memory methods
    def add_context(self, context_id: str, context: Dict[str, Any], ttl: int = 2592000) -> bool:
        """Add context to context memory."""
        return self.context.add_context(context_id, context, ttl)

    def get_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve context from context memory."""
        return self.context.get_context(context_id)

    def retrieve_relevant_contexts(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant contexts using semantic search."""
        return self.context.retrieve_relevant(query, top_k)

    def update_context(self, context_id: str, updates: Dict[str, Any]) -> bool:
        """Update context in context memory."""
        return self.context.update_context(context_id, updates)

    def delete_context(self, context_id: str) -> bool:
        """Delete context from context memory."""
        return self.context.delete_context(context_id)

    # Unified memory operations
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics from all memory systems."""
        return {
            "short_term": self.short_term.get_memory_stats(),
            "long_term": "Weaviate stats not implemented",  # TODO: Add Weaviate stats
            "context": self.context.get_memory_stats()
        }

    def clear_memory(self, memory_type: str = "all") -> Dict[str, int]:
        """Clear memory from specified memory type(s)."""
        cleared = {}

        if memory_type in ["all", "short_term"]:
            cleared["short_term"] = self.short_term.clear_expired()

        if memory_type in ["all", "context"]:
            cleared["context"] = self.context.clear_memory()

        # Long-term memory clearing not implemented (would require Weaviate API)
        cleared["long_term"] = 0

        return cleared

    def search_memory(self, query: str, memory_types: List[str] = ["context", "long_term"], top_k: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Search across multiple memory types."""
        results = {}

        if "context" in memory_types:
            results["context"] = self.context.retrieve_relevant(query, top_k)

        if "long_term" in memory_types:
            # For long-term memory, use Weaviate's semantic search
            similar_cases = self.long_term.query_similar_cases(query, top_k)
            results["long_term"] = similar_cases

        return results

    def store_unified(self, data_type: str, data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """
        Store data in appropriate memory system based on data type.

        Args:
            data_type: Type of data ("session", "interaction", "state", "case", "context")
            data: Data to store
            ttl: Time-to-live for temporary data

        Returns:
            bool: True if successful, False otherwise
        """
        ttl = ttl or 3600  # Default TTL: 1 hour

        if data_type == "session":
            return self.store_session(data["session_id"], data["data"], ttl)
        elif data_type == "interaction":
            return self.store_interaction(data["interaction_id"], data["data"], ttl)
        elif data_type == "state":
            return self.store_state(data["state_key"], data["data"], ttl)
        elif data_type == "case":
            return bool(self.store_case(
                data["case_id"],
                data["content"],
                data["context"],
                data["domain_tags"],
                data.get("metadata")
            ))
        elif data_type == "context":
            return self.add_context(data["context_id"], data["data"], ttl)
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def retrieve_unified(self, data_type: str, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from appropriate memory system.

        Args:
            data_type: Type of data ("session", "interaction", "state", "case", "context")
            identifier: Unique identifier

        Returns:
            Retrieved data or None if not found
        """
        if data_type == "session":
            return self.get_session(identifier)
        elif data_type == "interaction":
            return self.get_interaction(identifier)
        elif data_type == "state":
            return self.get_state(identifier)
        elif data_type == "case":
            # For cases, we need to query Weaviate
            # This is a simplified approach - in practice, you'd need more specific querying
            return {"case_id": identifier, "status": "retrieved from Weaviate"}
        elif data_type == "context":
            return self.get_context(identifier)
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass

# Global memory manager instance for convenience
memory_manager = MemoryManager()



