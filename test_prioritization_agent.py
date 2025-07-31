





"""
Test for Prioritization Agent
"""

import unittest
from agents.prioritization import PrioritizationAgent

class TestPrioritizationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PrioritizationAgent()

    def test_basic_prioritization(self):
        """Test basic prioritization with complete data"""
        task = {
            "task_id": "task-123",
            "title": "Implement API authentication",
            "description": "Add OAuth2 authentication to our API",
            "reach": 500,
            "impact": 8,
            "confidence": 0.9,
            "effort": 3,
            "urgency": 7,
            "is_blocking": True,
            "is_dependency": True,
            "blocks_count": 3
        }

        result = self.agent.prioritize(task)

        # Verify structure
        self.assertIn("task_id", result)
        self.assertIn("score", result)
        self.assertIn("criticality", result)
        self.assertIn("is_bottleneck", result)
        self.assertIn("bottlenecks", result)
        self.assertIn("reasoning", result)
        self.assertIn("explanation", result)
        self.assertIn("timestamp", result)

        # Verify values
        self.assertEqual(result["task_id"], "task-123")
        self.assertEqual(result["score"]["score_type"], "RICE")
        self.assertGreater(result["score"]["score"], 0)
        self.assertIn(result["criticality"], ["critical", "high", "medium", "low"])
        self.assertTrue(result["is_bottleneck"])
        self.assertGreater(len(result["bottlenecks"]), 0)
        self.assertGreater(len(result["reasoning"]), 0)

    def test_missing_parameters(self):
        """Test prioritization with missing parameters"""
        task = {
            "task_id": "task-456",
            "title": "Fix UI bug",
            "description": "Button alignment issue on mobile"
        }

        result = self.agent.prioritize(task)

        # Should still work with estimated parameters
        self.assertGreater(result["score"]["score"], 0)
        self.assertIn(result["criticality"], ["critical", "high", "medium", "low"])

    def test_bottleneck_detection(self):
        """Test bottleneck detection"""
        task = {
            "task_id": "task-789",
            "title": "Critical security fix",
            "description": "Fix SQL injection vulnerability",
            "reach": 1000,
            "impact": 9,
            "confidence": 0.95,
            "effort": 5,
            "blocks_count": 4
        }

        result = self.agent.prioritize(task)

        # Should detect bottleneck due to high blocks_count
        self.assertTrue(result["is_bottleneck"])
        self.assertIn("Blocks 4 other tasks", result["bottlenecks"])

    def test_criticality_classification(self):
        """Test criticality classification"""
        # High impact, high urgency, blocking task
        task = {
            "task_id": "task-crit",
            "title": "Production outage",
            "description": "Server crash affecting all users",
            "impact": 10,
            "urgency": 10,
            "is_blocking": True,
            "is_dependency": True,
            "effort": 2
        }

        result = self.agent.prioritize(task)
        self.assertEqual(result["criticality"], "critical")

        # Low impact, low urgency task
        task = {
            "task_id": "task-low",
            "title": "Minor UI tweak",
            "description": "Adjust button color",
            "impact": 2,
            "urgency": 1,
            "effort": 1
        }

        result = self.agent.prioritize(task)
        self.assertEqual(result["criticality"], "low")

    def test_configuration(self):
        """Test configurable thresholds"""
        # Test custom thresholds
        agent = PrioritizationAgent()
        agent.configure_thresholds(critical_threshold=10.0, high_threshold=7.0, medium_threshold=5.0)
        agent.configure_bottleneck_thresholds(score_threshold=4.0, effort_impact_ratio=0.6)

        # This should now be classified differently with stricter thresholds
        task = {
            "task_id": "task-config",
            "title": "Normal task",
            "description": "Regular development task",
            "impact": 6,
            "urgency": 4,
            "effort": 3
        }

        result = agent.prioritize(task)
        # With stricter thresholds, this might be medium instead of high
        self.assertIn(result["criticality"], ["high", "medium"])

    def test_enhanced_reasoning(self):
        """Test enhanced reasoning and explanations"""
        task = {
            "task_id": "task-reason",
            "title": "Critical security vulnerability",
            "description": "Fix SQL injection in user authentication",
            "impact": 9,
            "urgency": 8,
            "effort": 4,
            "is_blocking": True,
            "blocks_count": 2
        }

        result = self.agent.prioritize(task)

        # Check for detailed reasoning
        reasoning_text = " ".join(result["reasoning"])
        self.assertIn("high impact", reasoning_text)
        self.assertIn("high urgency", reasoning_text)
        self.assertIn("blocks other tasks", reasoning_text)
        self.assertIn("contains risk keywords", reasoning_text)

        # Check explanation - the explanation is in reasoning, not explanation field
        self.assertIn("critical", result["explanation"])

if __name__ == "__main__":
    unittest.main()





