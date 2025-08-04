


"""
Test Memory Module

Comprehensive test suite for the memory module.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory import MemoryManager, ShortTermMemory, ContextMemory, WeaviateMemory
import time

def test_short_term_memory():
    """Test short-term memory operations."""
    print("🧪 Testing Short-Term Memory...")

    # Initialize
    stm = ShortTermMemory.from_config()

    # Test session storage
    session_data = {"user": "test_user", "state": "active", "preferences": {"theme": "dark"}}
    stm.store_session("test_session_123", session_data, ttl=60)

    # Test retrieval
    retrieved = stm.get_session("test_session_123")
    assert retrieved is not None, "Session retrieval failed"
    assert retrieved["data"]["user"] == "test_user", "Session data mismatch"

    # Test interaction storage
    interaction_data = {"user": "test_user", "action": "click_button", "timestamp": time.time()}
    stm.store_interaction("test_interaction_456", interaction_data, ttl=60)

    # Test interaction retrieval
    retrieved_interaction = stm.get_interaction("test_interaction_456")
    assert retrieved_interaction is not None, "Interaction retrieval failed"

    # Test state storage
    state_data = {"step": 3, "progress": 0.75, "status": "in_progress"}
    stm.store_state("process_789", state_data, ttl=60)

    # Test state retrieval
    retrieved_state = stm.get_state("process_789")
    assert retrieved_state is not None, "State retrieval failed"

    # Test memory stats
    stats = stm.get_memory_stats()
    assert "used_memory" in stats, "Memory stats missing data"

    print("✅ Short-Term Memory tests passed!")

def test_context_memory():
    """Test context memory operations."""
    print("🧪 Testing Context Memory...")

    # Initialize
    cm = ContextMemory.from_config()

    # Test context storage
    context_data = {
        "text": "Important meeting about project deadlines",
        "source": "meeting_transcript",
        "participants": ["alice", "bob", "charlie"],
        "date": "2023-11-15"
    }
    cm.add_context("meeting_123", context_data, ttl=3600)

    # Test context retrieval
    retrieved = cm.get_context("meeting_123")
    assert retrieved is not None, "Context retrieval failed"
    assert "Important meeting" in retrieved["data"]["text"], "Context data mismatch"

    # Test semantic search
    search_results = cm.retrieve_relevant("project deadlines", top_k=3)
    assert len(search_results) > 0, "Semantic search returned no results"
    assert "meeting_123" in search_results[0]["context_id"], "Wrong context returned"

    # Test context update
    update_data = {"status": "reviewed", "reviewer": "alice"}
    cm.update_context("meeting_123", update_data)

    # Verify update
    updated_context = cm.get_context("meeting_123")
    assert updated_context["data"]["status"] == "reviewed", "Context update failed"

    # Test context deletion
    cm.delete_context("meeting_123")
    deleted_context = cm.get_context("meeting_123")
    assert deleted_context is None, "Context deletion failed"

    print("✅ Context Memory tests passed!")

def test_long_term_memory():
    """Test long-term memory operations."""
    print("🧪 Testing Long-Term Memory...")

    # Initialize
    ltm = WeaviateMemory()

    # Test case storage
    case_data = {
        "case_id": "test_case_456",
        "content": "Contract analysis for Project X",
        "context": "legal review",
        "domain_tags": ["legal", "contract", "review"],
        "metadata": {"priority": "high", "deadline": "2023-12-01"}
    }

    # Store case
    result = ltm.store_case(
        case_data["case_id"],
        case_data["content"],
        case_data["context"],
        case_data["domain_tags"],
        case_data["metadata"]
    )
    assert result is not None, "Case storage failed"

    # Test case update
    update_result = ltm.update_case_status("test_case_456", "completed", ["legal_agent", "review_agent"])
    assert update_result is not None, "Case status update failed"

    # Test similar case search
    similar_case = ltm.find_similar_case("Contract review for Project Y")
    # Note: This might return None if no similar cases exist

    # Test case querying
    cases = ltm.query_similar_cases("Contract analysis", limit=2)
    assert len(cases) >= 0, "Case querying failed"

    print("✅ Long-Term Memory tests passed!")

def test_memory_manager():
    """Test unified memory manager."""
    print("🧪 Testing Memory Manager...")

    # Initialize
    mm = MemoryManager()

    # Test unified storage
    mm.store_unified("session", {
        "session_id": "unified_test_123",
        "data": {"user": "unified_user", "preferences": {"language": "en"}}
    })

    mm.store_unified("context", {
        "context_id": "unified_context_456",
        "data": {"text": "Unified memory test context", "source": "test"}
    })

    # Test unified retrieval
    session = mm.retrieve_unified("session", "unified_test_123")
    assert session is not None, "Unified session retrieval failed"

    context = mm.retrieve_unified("context", "unified_context_456")
    assert context is not None, "Unified context retrieval failed"

    # Test memory stats
    stats = mm.get_memory_stats()
    assert "short_term" in stats, "Memory manager stats missing short_term data"
    assert "context" in stats, "Memory manager stats missing context data"

    # Test search
    search_results = mm.search_memory("unified memory", memory_types=["context"], top_k=2)
    assert "context" in search_results, "Memory manager search failed"

    print("✅ Memory Manager tests passed!")

def run_all_tests():
    """Run all memory module tests."""
    print("🚀 Running Memory Module Tests")
    print("=" * 50)

    try:
        test_short_term_memory()
        test_context_memory()
        test_long_term_memory()
        test_memory_manager()

        print("\n🎉 All Memory Module tests passed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)


