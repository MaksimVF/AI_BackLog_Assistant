


import requests
from typing import Optional, Dict, Any, List

class GitHubConnectorAgent:
    """Agent for interacting with GitHub API"""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def get_issue(self, owner: str, repo: str, issue_number: int) -> Optional[Dict]:
        """Get a specific GitHub issue"""
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def create_issue(self, owner: str, repo: str, title: str, body: str, labels: List[str] = None) -> Optional[Dict]:
        """Create a new GitHub issue"""
        url = f'{self.base_url}/repos/{owner}/{repo}/issues'
        payload = {
            'title': title,
            'body': body,
            'labels': labels or []
        }
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        return None

    def add_comment(self, owner: str, repo: str, issue_number: int, body: str) -> Optional[Dict]:
        """Add a comment to an issue"""
        url = f'{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments'
        payload = {'body': body}
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        return None

    def get_pull_request(self, owner: str, repo: str, pr_number: int) -> Optional[Dict]:
        """Get a specific pull request"""
        url = f'{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def list_issues(self, owner: str, repo: str, state: str = 'open') -> List[Dict]:
        """List issues in a repository"""
        url = f'{self.base_url}/repos/{owner}/{repo}/issues'
        params = {'state': state}
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        return []

    def search_issues(self, query: str) -> List[Dict]:
        """Search for issues across repositories"""
        url = f'{self.base_url}/search/issues'
        params = {'q': query}
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json().get('items', [])
        return []

    def get_repo(self, owner: str, repo: str) -> Optional[Dict]:
        """Get repository information"""
        url = f'{self.base_url}/repos/{owner}/{repo}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def get_commits(self, owner: str, repo: str, sha: str = None, path: str = None, since: str = None) -> List[Dict]:
        """Get commits from a repository"""
        url = f'{self.base_url}/repos/{owner}/{repo}/commits'
        params = {}
        if sha:
            params['sha'] = sha
        if path:
            params['path'] = path
        if since:
            params['since'] = since

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        return []

    def get_file_content(self, owner: str, repo: str, path: str, ref: str = None) -> Optional[str]:
        """Get content of a file from repository"""
        url = f'{self.base_url}/repos/{owner}/{repo}/contents/{path}'
        params = {}
        if ref:
            params['ref'] = ref

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            content = response.json().get('content', '')
            if content:
                import base64
                return base64.b64decode(content).decode('utf-8')
        return None

# Example usage
if __name__ == '__main__':
    # You would get this token from your OAuth2 flow
    token = 'your_github_access_token'
    github = GitHubConnectorAgent(token)

    # Example: Get an issue
    issue = github.get_issue('MaksimVF', 'AI_BackLog_Assistant', 1)
    print(issue)

    # Example: Create an issue
    new_issue = github.create_issue(
        'MaksimVF',
        'AI_BackLog_Assistant',
        'Test Issue from GitHubConnectorAgent',
        'This is a test issue created by the GitHubConnectorAgent'
    )
    print(new_issue)

