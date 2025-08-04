

"""
Memory Module

Provides unified access to different memory systems:
- Short-term memory (Redis)
- Long-term memory (Weaviate)
- Context memory (Redis + semantic search)

Usage:
    from memory import MemoryManager

    memory = MemoryManager()
    memory.store_short_term("session_123", {"user": "john", "state": "active"})
    memory.store_long_term("case_456", "Contract analysis", "legal", ["contract", "analysis"])
    memory.store_context({"text": "Important meeting notes", "source": "meeting_789"})
"""

from .memory_manager import MemoryManager
from .short_term_memory import ShortTermMemory
from .context_memory import ContextMemory
from .weaviate_client import WeaviateMemory

__all__ = ["MemoryManager", "ShortTermMemory", "ContextMemory", "WeaviateMemory"]

