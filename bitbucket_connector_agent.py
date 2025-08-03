



import requests
from typing import Optional, Dict, Any, List

class BitbucketConnectorAgent:
    """Agent for interacting with Bitbucket API"""

    def __init__(self, access_token: str, workspace: str):
        self.access_token = access_token
        self.workspace = workspace
        self.base_url = 'https://api.bitbucket.org/2.0'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }

    def get_issue(self, repo_slug: str, issue_id: int) -> Optional[Dict]:
        """Get a specific Bitbucket issue"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}/issues/{issue_id}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def create_issue(self, repo_slug: str, title: str, content: str, kind: str = 'bug') -> Optional[Dict]:
        """Create a new Bitbucket issue"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}/issues'
        payload = {
            'title': title,
            'content': {
                'raw': content
            },
            'kind': kind
        }
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        return None

    def add_comment(self, repo_slug: str, issue_id: int, content: str) -> Optional[Dict]:
        """Add a comment to an issue"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}/issues/{issue_id}/comments'
        payload = {
            'content': {
                'raw': content
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        return None

    def get_pull_request(self, repo_slug: str, pr_id: int) -> Optional[Dict]:
        """Get a specific pull request"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}/pullrequests/{pr_id}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def list_issues(self, repo_slug: str, q: str = None) -> List[Dict]:
        """List issues in a repository"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}/issues'
        params = {}
        if q:
            params['q'] = q

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json().get('values', [])
        return []

    def search_issues(self, query: str) -> List[Dict]:
        """Search for issues across repositories"""
        # Bitbucket doesn't have a global search API, so we'd need to implement
        # repo-by-repo search
        return []

    def get_repo(self, repo_slug: str) -> Optional[Dict]:
        """Get repository information"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def get_commits(self, repo_slug: str, since: str = None) -> List[Dict]:
        """Get commits from a repository"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}/commit'
        params = {}
        if since:
            params['since'] = since

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json().get('values', [])
        return []

    def get_file_content(self, repo_slug: str, file_path: str, commit: str = None) -> Optional[str]:
        """Get content of a file from repository"""
        url = f'{self.base_url}/repositories/{self.workspace}/{repo_slug}/src/{commit or "main"}/{file_path}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.text
        return None

# Example usage
if __name__ == '__main__':
    # You would get this token from your OAuth2 flow
    token = 'your_bitbucket_access_token'
    workspace = 'your_workspace'
    bitbucket = BitbucketConnectorAgent(token, workspace)

    # Example: Get an issue
    issue = bitbucket.get_issue('your_repo_slug', 1)
    print(issue)

    # Example: Create an issue
    new_issue = bitbucket.create_issue(
        'your_repo_slug',
        'Test Issue from BitbucketConnectorAgent',
        'This is a test issue created by the BitbucketConnectorAgent'
    )
    print(new_issue)




