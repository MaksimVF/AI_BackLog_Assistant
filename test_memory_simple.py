



"""
Simple Memory Module Test

Basic test for memory module functionality without SentenceTransformer dependency.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory import ShortTermMemory, MemoryManager

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
    interaction_data = {"user": "test_user", "action": "click_button", "timestamp": "2023-01-01"}
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

    # Test unified retrieval
    session = mm.retrieve_unified("session", "unified_test_123")
    assert session is not None, "Unified session retrieval failed"

    # Test memory stats
    stats = mm.get_memory_stats()
    assert "short_term" in stats, "Memory manager stats missing short_term data"

    print("✅ Memory Manager tests passed!")

def run_simple_tests():
    """Run simple memory module tests."""
    print("🚀 Running Simple Memory Module Tests")
    print("=" * 50)

    try:
        test_short_term_memory()
        test_memory_manager()

        print("\n🎉 All Simple Memory Module tests passed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)



