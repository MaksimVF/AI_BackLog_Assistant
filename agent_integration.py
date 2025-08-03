


from github_connector_agent import GitHubConnectorAgent
from typing import Dict, Any

class CategorizationAgent:
    """Agent for categorizing GitHub issues"""

    def __init__(self, github_connector: GitHubConnectorAgent):
        self.github = github_connector

    def process_issue(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        """Process and categorize a GitHub issue"""
        issue = self.github.get_issue(owner, repo, issue_number)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        # Analyze the issue (this would be your AI logic)
        title = issue.get('title', '')
        body = issue.get('body', '')
        labels = issue.get('labels', [])

        # Simple categorization logic (replace with your AI model)
        category = self._categorize_issue(title, body)

        # Add category as a label
        category_label = f'category:{category}'
        if not any(label['name'] == category_label for label in labels):
            self.github.add_comment(
                owner,
                repo,
                issue_number,
                f'This issue has been categorized as: {category}'
            )

        return {
            'status': 'success',
            'issue_number': issue_number,
            'category': category,
            'title': title
        }

    def _categorize_issue(self, title: str, body: str) -> str:
        """Simple categorization logic"""
        # This is where you would integrate your AI model
        # For now, we'll use simple keyword matching
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

class PrioritizationAgent:
    """Agent for prioritizing GitHub issues"""

    def __init__(self, github_connector: GitHubConnectorAgent):
        self.github = github_connector

    def prioritize_issue(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        """Prioritize a GitHub issue using RICE/ICE methodology"""
        issue = self.github.get_issue(owner, repo, issue_number)

        if not issue:
            return {'status': 'error', 'message': 'Issue not found'}

        # Simple prioritization logic (replace with your AI model)
        priority = self._calculate_priority(issue)

        # Add priority label
        priority_label = f'priority:{priority}'
        self.github.add_comment(
            owner,
            repo,
            issue_number,
            f'This issue has been prioritized as: {priority}'
        )

        return {
            'status': 'success',
            'issue_number': issue_number,
            'priority': priority,
            'title': issue.get('title')
        }

    def _calculate_priority(self, issue: Dict) -> str:
        """Simple RICE prioritization logic"""
        # This would be your actual prioritization algorithm
        # For now, we'll use a simple approach based on issue age and comments

        # Get issue age in days
        created_at = issue.get('created_at')
        # In a real implementation, you'd calculate the actual age

        # Get number of comments
        comments = issue.get('comments', 0)

        # Simple scoring
        score = min(comments, 10)  # Max 10 points for comments

        if score >= 8:
            return 'high'
        elif score >= 4:
            return 'medium'
        else:
            return 'low'

# Example usage
if __name__ == '__main__':
    # Initialize GitHub connector
    token = 'your_github_access_token'
    github = GitHubConnectorAgent(token)

    # Initialize agents
    categorization_agent = CategorizationAgent(github)
    prioritization_agent = PrioritizationAgent(github)

    # Process an issue
    result = categorization_agent.process_issue('MaksimVF', 'AI_BackLog_Assistant', 1)
    print('Categorization result:', result)

    # Prioritize an issue
    priority_result = prioritization_agent.prioritize_issue('MaksimVF', 'AI_BackLog_Assistant', 1)
    print('Prioritization result:', priority_result)


