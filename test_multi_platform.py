



import unittest
from github_connector_agent import GitHubConnectorAgent
from gitlab_connector_agent import GitLabConnectorAgent
from bitbucket_connector_agent import BitbucketConnectorAgent
from multi_platform_integration import UnifiedCategorizationAgent, UnifiedPrioritizationAgent

class TestMultiPlatformIntegration(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        # Use mock tokens for testing
        self.github_token = 'mock_github_token'
        self.gitlab_token = 'mock_gitlab_token'
        self.bitbucket_token = 'mock_bitbucket_token'
        self.workspace = 'test_workspace'

        # Initialize connectors
        self.github = GitHubConnectorAgent(self.github_token)
        self.gitlab = GitLabConnectorAgent(self.gitlab_token)
        self.bitbucket = BitbucketConnectorAgent(self.bitbucket_token, self.workspace)

    def test_github_integration(self):
        """Test GitHub integration"""
        categorizer = UnifiedCategorizationAgent(self.github)
        prioritizer = UnifiedPrioritizationAgent(self.github)

        self.assertEqual(categorizer.platform, 'github')
        self.assertEqual(prioritizer.platform, 'github')

    def test_gitlab_integration(self):
        """Test GitLab integration"""
        categorizer = UnifiedCategorizationAgent(self.gitlab)
        prioritizer = UnifiedPrioritizationAgent(self.gitlab)

        self.assertEqual(categorizer.platform, 'gitlab')
        self.assertEqual(prioritizer.platform, 'gitlab')

    def test_bitbucket_integration(self):
        """Test Bitbucket integration"""
        categorizer = UnifiedCategorizationAgent(self.bitbucket)
        prioritizer = UnifiedPrioritizationAgent(self.bitbucket)

        self.assertEqual(categorizer.platform, 'bitbucket')
        self.assertEqual(prioritizer.platform, 'bitbucket')

    def test_categorization_methods(self):
        """Test that categorization methods exist"""
        categorizer = UnifiedCategorizationAgent(self.github)

        self.assertTrue(hasattr(categorizer, 'process_issue'))
        self.assertTrue(hasattr(categorizer, '_categorize_issue'))

    def test_prioritization_methods(self):
        """Test that prioritization methods exist"""
        prioritizer = UnifiedPrioritizationAgent(self.github)

        self.assertTrue(hasattr(prioritizer, 'prioritize_issue'))
        self.assertTrue(hasattr(prioritizer, '_calculate_priority'))

if __name__ == '__main__':
    unittest.main()



