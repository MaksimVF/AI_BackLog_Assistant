



from typing import Dict, Any, Union
from github_connector_agent import GitHubConnectorAgent
from gitlab_connector_agent import GitLabConnectorAgent
from bitbucket_connector_agent import BitbucketConnectorAgent

class UnifiedCategorizationAgent:
    """Agent for categorizing issues across different platforms"""

    def __init__(self, connector: Union[GitHubConnectorAgent, GitLabConnectorAgent, BitbucketConnectorAgent]):
        self.connector = connector
        self.platform = self._detect_platform()

    def _detect_platform(self) -> str:
        """Detect which platform the connector is for"""
        if isinstance(self.connector, GitHubConnectorAgent):
            return 'github'
        elif isinstance(self.connector, GitLabConnectorAgent):
            return 'gitlab'
        elif isinstance(self.connector, BitbucketConnectorAgent):
            return 'bitbucket'
        else:
            return 'unknown'

    def process_issue(self, *args, **kwargs) -> Dict[str, Any]:
        """Process and categorize an issue based on the platform"""
        if self.platform == 'github':
            return self._process_github_issue(*args, **kwargs)
        elif self.platform == 'gitlab':
            return self._process_gitlab_issue(*args, **kwargs)
        elif self.platform == 'bitbucket':
            return self._process_bitbucket_issue(*args, **kwargs)
        else:
            return {'status': 'error', 'message': 'Unsupported platform'}

    def _process_github_issue(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        """Process a GitHub issue"""
        issue = self.connector.get_issue(owner, repo, issue_number)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        category = self._categorize_issue(issue.get('title', ''), issue.get('body', ''))
        return {
            'status': 'success',
            'platform': 'github',
            'issue_number': issue_number,
            'category': category,
            'title': issue.get('title')
        }

    def _process_gitlab_issue(self, project_id: str, issue_id: int) -> Dict[str, Any]:
        """Process a GitLab issue"""
        issue = self.connector.get_issue(project_id, issue_id)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        category = self._categorize_issue(issue.get('title', ''), issue.get('description', ''))
        return {
            'status': 'success',
            'platform': 'gitlab',
            'issue_id': issue_id,
            'category': category,
            'title': issue.get('title')
        }

    def _process_bitbucket_issue(self, repo_slug: str, issue_id: int) -> Dict[str, Any]:
        """Process a Bitbucket issue"""
        issue = self.connector.get_issue(repo_slug, issue_id)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        category = self._categorize_issue(issue.get('title', ''), issue.get('content', {}).get('raw', ''))
        return {
            'status': 'success',
            'platform': 'bitbucket',
            'issue_id': issue_id,
            'category': category,
            'title': issue.get('title')
        }

    def _categorize_issue(self, title: str, body: str) -> str:
        """Simple categorization logic"""
        keywords = {
            'bug': ['bug', 'error', 'issue', 'problem'],
            'feature': ['feature', 'request', 'enhancement', 'new'],
            'question': ['question', 'how', 'what', 'why', '?'],
            'documentation': ['doc', 'documentation', 'docs', 'guide']
        }

        text = (title + ' ' + body).lower()

        for category, kws in keywords.items():
            if any(kw in text for kw in kws):
                return category

        return 'other'

class UnifiedPrioritizationAgent:
    """Agent for prioritizing issues across different platforms"""

    def __init__(self, connector: Union[GitHubConnectorAgent, GitLabConnectorAgent, BitbucketConnectorAgent]):
        self.connector = connector
        self.platform = self._detect_platform()

    def _detect_platform(self) -> str:
        """Detect which platform the connector is for"""
        if isinstance(self.connector, GitHubConnectorAgent):
            return 'github'
        elif isinstance(self.connector, GitLabConnectorAgent):
            return 'gitlab'
        elif isinstance(self.connector, BitbucketConnectorAgent):
            return 'bitbucket'
        else:
            return 'unknown'

    def prioritize_issue(self, *args, **kwargs) -> Dict[str, Any]:
        """Prioritize an issue based on the platform"""
        if self.platform == 'github':
            return self._prioritize_github_issue(*args, **kwargs)
        elif self.platform == 'gitlab':
            return self._prioritize_gitlab_issue(*args, **kwargs)
        elif self.platform == 'bitbucket':
            return self._prioritize_bitbucket_issue(*args, **kwargs)
        else:
            return {'status': 'error', 'message': 'Unsupported platform'}

    def _prioritize_github_issue(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        """Prioritize a GitHub issue"""
        issue = self.connector.get_issue(owner, repo, issue_number)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        priority = self._calculate_priority(issue)
        return {
            'status': 'success',
            'platform': 'github',
            'issue_number': issue_number,
            'priority': priority,
            'title': issue.get('title')
        }

    def _prioritize_gitlab_issue(self, project_id: str, issue_id: int) -> Dict[str, Any]:
        """Prioritize a GitLab issue"""
        issue = self.connector.get_issue(project_id, issue_id)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        priority = self._calculate_priority(issue)
        return {
            'status': 'success',
            'platform': 'gitlab',
            'issue_id': issue_id,
            'priority': priority,
            'title': issue.get('title')
        }

    def _prioritize_bitbucket_issue(self, repo_slug: str, issue_id: int) -> Dict[str, Any]:
        """Prioritize a Bitbucket issue"""
        issue = self.connector.get_issue(repo_slug, issue_id)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        priority = self._calculate_priority(issue)
        return {
            'status': 'success',
            'platform': 'bitbucket',
            'issue_id': issue_id,
            'priority': priority,
            'title': issue.get('title')
        }

    def _calculate_priority(self, issue: Dict) -> str:
        """Simple RICE prioritization logic"""
        # Simple scoring based on comments
        comments = issue.get('comments', 0) if 'comments' in issue else 0

        score = min(comments, 10)  # Max 10 points for comments

        if score >= 8:
            return 'high'
        elif score >= 4:
            return 'medium'
        else:
            return 'low'

# Example usage
if __name__ == '__main__':
    # Example with GitHub
    github_token = 'your_github_token'
    github = GitHubConnectorAgent(github_token)
    github_categorizer = UnifiedCategorizationAgent(github)
    github_prioritizer = UnifiedPrioritizationAgent(github)

    # Example with GitLab
    gitlab_token = 'your_gitlab_token'
    gitlab = GitLabConnectorAgent(gitlab_token)
    gitlab_categorizer = UnifiedCategorizationAgent(gitlab)
    gitlab_prioritizer = UnifiedPrioritizationAgent(gitlab)

    # Example with Bitbucket
    bitbucket_token = 'your_bitbucket_token'
    workspace = 'your_workspace'
    bitbucket = BitbucketConnectorAgent(bitbucket_token, workspace)
    bitbucket_categorizer = UnifiedCategorizationAgent(bitbucket)
    bitbucket_prioritizer = UnifiedPrioritizationAgent(bitbucket)

    # Test categorization
    print('GitHub categorization:', github_categorizer.process_issue('owner', 'repo', 1))
    print('GitLab categorization:', gitlab_categorizer.process_issue('project_id', 1))
    print('Bitbucket categorization:', bitbucket_categorizer.process_issue('repo_slug', 1))

    # Test prioritization
    print('GitHub prioritization:', github_prioritizer.prioritize_issue('owner', 'repo', 1))
    print('GitLab prioritization:', gitlab_prioritizer.prioritize_issue('project_id', 1))
    print('Bitbucket prioritization:', bitbucket_prioritizer.prioritize_issue('repo_slug', 1))




