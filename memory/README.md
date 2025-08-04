


# 🧠 Memory Module

## Overview

The Memory Module provides a comprehensive memory system for the AI Backlog Assistant, consisting of three main components:

1. **Short-term Memory** (Redis) - Fast, temporary storage for sessions, interactions, and state
2. **Long-term Memory** (Weaviate) - Persistent, semantic storage for cases and knowledge
3. **Context Memory** (Redis + Semantic Search) - Context-aware memory with semantic retrieval

## Features

- **Unified Interface**: Single access point for all memory operations
- **Semantic Search**: Context-aware retrieval using embeddings
- **Persistence**: Redis and Weaviate backends for reliable storage
- **Scalability**: Designed to handle large volumes of data
- **Performance**: Optimized for fast read/write operations

## Architecture

```
MemoryManager (Unified Interface)
      │           │           │
      │           │           │
ShortTermMemory  WeaviateMemory  ContextMemory
      │           │           │
      │           │           │
    Redis       Weaviate     Redis + SentenceTransformer
```

## Installation

The memory module requires:
- Redis server
- Weaviate server
- SentenceTransformer (for semantic search)

```bash
pip install redis weaviate-client sentence-transformers
```

## Usage

### Basic Usage

```python
from memory import MemoryManager

# Initialize memory manager
memory = MemoryManager()

# Store session data (short-term)
memory.store_session("user_123", {"user": "john", "state": "active"})

# Store case data (long-term)
memory.store_case("case_456", "Contract analysis", "legal", ["contract"])

# Store context (context memory)
memory.add_context("meeting_789", {"text": "Project meeting notes"})

# Search across all memory types
results = memory.search_memory("contract review")
```

### Short-term Memory

```python
# Store temporary state
memory.store_state("process_123", {"step": 2, "status": "processing"})

# Retrieve session
session = memory.get_session("user_123")

# Store interaction
memory.store_interaction("click_456", {"action": "button_click", "timestamp": "2023-01-01"})
```

### Context Memory

```python
# Add context with semantic capabilities
memory.add_context("discussion_789", {
    "text": "Team discussion about project timeline",
    "participants": ["alice", "bob"]
})

# Retrieve relevant contexts
relevant = memory.retrieve_relevant_contexts("project timeline", top_k=3)
```

### Long-term Memory

```python
# Store case for long-term reference
memory.store_case("legal_001", "NDA review", "legal", ["contract", "nda"])

# Find similar cases
similar_case = memory.find_similar_case("Contract review for new client")
```

## Configuration

Memory systems can be configured via environment variables:

- `REDIS_URL`: Redis connection URL (default: `redis://localhost:6379/0`)
- `WEAVIATE_URL`: Weaviate connection URL (default: `http://localhost:8080`)
- `EMBEDDING_MODEL_NAME`: SentenceTransformer model (default: `all-MiniLM-L6-v2`)

## Testing

Run the comprehensive test suite:

```bash
python test_memory_module.py
```

## Performance Considerations

- **Redis**: Optimized for fast read/write operations
- **Weaviate**: Optimized for semantic search and vector storage
- **Memory Management**: Automatic expiration and cleanup

## Future Enhancements

- Add memory compression for large datasets
- Implement memory tiering (hot/warm/cold storage)
- Add memory analytics and visualization
- Implement memory-based agent recommendations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details


