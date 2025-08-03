


import unittest
from github_connector_agent import GitHubConnectorAgent
from agent_integration import CategorizationAgent, PrioritizationAgent

class TestGitHubIntegration(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        # Use a test token (in a real scenario, you'd use a mock)
        self.token = 'your_test_github_token'
        self.github = GitHubConnectorAgent(self.token)
        self.categorization_agent = CategorizationAgent(self.github)
        self.prioritization_agent = PrioritizationAgent(self.github)

    def test_github_connector(self):
        """Test GitHub connector basic functionality"""
        # Test getting a repository (use a public repo for testing)
        repo = self.github.get_repo('MaksimVF', 'AI_BackLog_Assistant')
        self.assertIsNotNone(repo)
        self.assertEqual(repo.get('full_name'), 'MaksimVF/AI_BackLog_Assistant')

    def test_categorization_agent(self):
        """Test categorization agent"""
        # This would work with a real issue in your repo
        # For testing, we'll just check that the methods exist
        self.assertTrue(hasattr(self.categorization_agent, 'process_issue'))
        self.assertTrue(hasattr(self.categorization_agent, '_categorize_issue'))

    def test_prioritization_agent(self):
        """Test prioritization agent"""
        # This would work with a real issue in your repo
        # For testing, we'll just check that the methods exist
        self.assertTrue(hasattr(self.prioritization_agent, 'prioritize_issue'))
        self.assertTrue(hasattr(self.prioritization_agent, '_calculate_priority'))

if __name__ == '__main__':
    unittest.main()


