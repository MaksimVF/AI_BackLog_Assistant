













"""
Test Feedback Agent
"""

from agents.service.feedback_agent import FeedbackAgent
from agents.service.mock_storage import InMemoryStorage

def test_feedback_agent_saves_feedback():
    """Test that FeedbackAgent saves feedback correctly"""
    storage = InMemoryStorage()
    agent = FeedbackAgent(storage)

    feedback = agent.run(
        task_id="T321",
        user_rating="positive",
        user_comment="Все отлично!",
        user_id="U123"
    )

    # Verify record was saved
    assert len(storage.feedback_logs) == 1
    saved = storage.feedback_logs[0]

    # Verify record contents
    assert saved["task_id"] == "T321"
    assert saved["rating"] == "positive"
    assert saved["comment"] == "Все отлично!"
    assert saved["user_id"] == "U123"
    assert "timestamp" in saved

def test_feedback_agent_without_comment():
    """Test FeedbackAgent without comment"""
    storage = InMemoryStorage()
    agent = FeedbackAgent(storage)

    feedback = agent.run(
        task_id="T321",
        user_rating="negative",
        user_id="U123"
    )

    assert len(storage.feedback_logs) == 1
    saved = storage.feedback_logs[0]
    assert saved["comment"] is None

def test_feedback_agent_without_user_id():
    """Test FeedbackAgent without user_id"""
    storage = InMemoryStorage()
    agent = FeedbackAgent(storage)

    feedback = agent.run(
        task_id="T321",
        user_rating="neutral",
        user_comment="No comment"
    )

    assert len(storage.feedback_logs) == 1
    saved = storage.feedback_logs[0]
    assert saved["user_id"] is None

if __name__ == "__main__":
    test_feedback_agent_saves_feedback()
    test_feedback_agent_without_comment()
    test_feedback_agent_without_user_id()
    print("All feedback agent tests passed!")













