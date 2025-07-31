












"""
Test Audit Agent
"""

from datetime import datetime
from agents.service.audit_agent import AuditAgent

from agents.service.mock_storage import InMemoryStorage

def test_audit_agent_saves_record():
    """Test that AuditAgent saves audit records correctly"""
    storage = InMemoryStorage()
    agent = AuditAgent(storage)

    result = agent.run(
        task_id="T123",
        inputs={"param1": "value1"},
        outputs={"result": "ok"},
        agent_chain=["InputCollector", "ScorerAgent"],
        user_id="U456"
    )

    # Verify record was saved
    assert len(storage.audit_logs) == 1
    saved = storage.audit_logs[0]

    # Verify record contents
    assert saved["task_id"] == "T123"
    assert saved["user_id"] == "U456"
    assert saved["agent_chain"] == ["InputCollector", "ScorerAgent"]
    assert "timestamp" in saved
    assert saved["inputs"] == {"param1": "value1"}
    assert saved["outputs"] == {"result": "ok"}

def test_audit_agent_without_user_id():
    """Test AuditAgent without user_id"""
    storage = InMemoryStorage()
    agent = AuditAgent(storage)

    result = agent.run(
        task_id="T123",
        inputs={"param1": "value1"},
        outputs={"result": "ok"},
        agent_chain=["InputCollector", "ScorerAgent"]
    )

    assert len(storage.audit_logs) == 1
    saved = storage.audit_logs[0]
    assert saved["user_id"] is None

if __name__ == "__main__":
    test_audit_agent_saves_record()
    test_audit_agent_without_user_id()
    print("All audit agent tests passed!")












