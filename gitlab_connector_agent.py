



import requests
from typing import Optional, Dict, Any, List

class GitLabConnectorAgent:
    """Agent for interacting with GitLab API"""

    def __init__(self, access_token: str, base_url: str = 'https://gitlab.com'):
        self.access_token = access_token
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def get_issue(self, project_id: str, issue_id: int) -> Optional[Dict]:
        """Get a specific GitLab issue"""
        url = f'{self.base_url}/api/v4/projects/{project_id}/issues/{issue_id}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def create_issue(self, project_id: str, title: str, description: str, labels: List[str] = None) -> Optional[Dict]:
        """Create a new GitLab issue"""
        url = f'{self.base_url}/api/v4/projects/{project_id}/issues'
        payload = {
            'title': title,
            'description': description,
            'labels': labels or []
        }
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        return None

    def add_comment(self, project_id: str, issue_id: int, body: str) -> Optional[Dict]:
        """Add a comment to an issue"""
        url = f'{self.base_url}/api/v4/projects/{project_id}/issues/{issue_id}/notes'
        payload = {'body': body}
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 201:
            return response.json()
        return None

    def get_merge_request(self, project_id: str, mr_id: int) -> Optional[Dict]:
        """Get a specific merge request"""
        url = f'{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def list_issues(self, project_id: str, state: str = 'opened') -> List[Dict]:
        """List issues in a project"""
        url = f'{self.base_url}/api/v4/projects/{project_id}/issues'
        params = {'state': state}
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        return []

    def search_issues(self, query: str) -> List[Dict]:
        """Search for issues across projects"""
        # GitLab doesn't have a global search API, so we'd need to implement
        # project-by-project search or use the GitLab search API
        return []

    def get_project(self, project_id: str) -> Optional[Dict]:
        """Get project information"""
        url = f'{self.base_url}/api/v4/projects/{project_id}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def get_commits(self, project_id: str, ref_name: str = None, since: str = None) -> List[Dict]:
        """Get commits from a project"""
        url = f'{self.base_url}/api/v4/projects/{project_id}/repository/commits'
        params = {}
        if ref_name:
            params['ref_name'] = ref_name
        if since:
            params['since'] = since

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        return []

    def get_file_content(self, project_id: str, file_path: str, ref: str = None) -> Optional[str]:
        """Get content of a file from project"""
        url = f'{self.base_url}/api/v4/projects/{project_id}/repository/files/{file_path}/raw'
        params = {}
        if ref:
            params['ref'] = ref

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.text
        return None

# Example usage
if __name__ == '__main__':
    # You would get this token from your OAuth2 flow
    token = 'your_gitlab_access_token'
    gitlab = GitLabConnectorAgent(token)

    # Example: Get an issue
    issue = gitlab.get_issue('your_project_id', 1)
    print(issue)

    # Example: Create an issue
    new_issue = gitlab.create_issue(
        'your_project_id',
        'Test Issue from GitLabConnectorAgent',
        'This is a test issue created by the GitLabConnectorAgent'
    )
    print(new_issue)



