

"""
Jira Client for integrating with Jira API.
"""

import os
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel, Field

class JiraConfig(BaseModel):
    """Configuration for Jira client."""
    base_url: str
    username: str
    api_token: str
    project_key: str

class JiraIssue(BaseModel):
    """Represents a Jira issue."""
    id: str
    key: str
    title: str = Field(alias="fields.summary")
    description: Optional[str] = Field(alias="fields.description")
    status: str = Field(alias="fields.status.name")
    priority: str = Field(alias="fields.priority.name")
    created_at: datetime = Field(alias="fields.created")
    updated_at: datetime = Field(alias="fields.updated")
    assignee: Optional[str] = Field(alias="fields.assignee.displayName")
    external_id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class JiraClient:
    """
    Client for interacting with Jira API.

    Features:
    - Fetch issues from Jira
    - Create/update issues
    - Sync with local task database
    - Handle authentication
    """

    def __init__(self, config: Optional[JiraConfig] = None):
        """
        Initialize Jira client.

        Args:
            config: Jira configuration. If None, will try to load from environment.
        """
        if config is None:
            config = self._load_config_from_env()

        self.config = config
        self.base_url = config.base_url.rstrip('/')
        self.auth = HTTPBasicAuth(config.username, config.api_token)
        self.project_key = config.project_key
        self.default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _load_config_from_env(self) -> JiraConfig:
        """Load configuration from environment variables."""
        return JiraConfig(
            base_url=os.getenv("JIRA_BASE_URL", "https://your-domain.atlassian.net"),
            username=os.getenv("JIRA_USERNAME", ""),
            api_token=os.getenv("JIRA_API_TOKEN", ""),
            project_key=os.getenv("JIRA_PROJECT_KEY", "PROJ")
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make HTTP request to Jira API."""
        url = f"{self.base_url}/rest/api/3/{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                auth=self.auth,
                headers=self.default_headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            raise JiraClientError(f"Jira API request failed: {str(e)}") from e

    def get_issue(self, issue_key: str) -> JiraIssue:
        """Get a single Jira issue by key."""
        data = self._make_request("GET", f"issue/{issue_key}")
        return JiraIssue(**data)

    def search_issues(self, jql: str, fields: Optional[List[str]] = None) -> List[JiraIssue]:
        """Search for issues using JQL."""
        params = {"jql": jql}
        if fields:
            params["fields"] = ",".join(fields)

        data = self._make_request("GET", "search", params=params)
        return [JiraIssue(**issue) for issue in data.get("issues", [])]

    def create_issue(self, title: str, description: str, issue_type: str = "Task",
                    priority: str = "Medium", **fields) -> JiraIssue:
        """Create a new Jira issue."""
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": title,
                "description": description,
                "issuetype": {"name": issue_type},
                **fields
            }
        }

        data = self._make_request("POST", "issue", json=payload)
        return JiraIssue(**data)

    def update_issue(self, issue_key: str, **fields) -> JiraIssue:
        """Update an existing Jira issue."""
        payload = {"fields": fields}
        data = self._make_request("PUT", f"issue/{issue_key}", json=payload)
        return JiraIssue(**data)

    def sync_issues(self, external_ids: List[str]) -> List[JiraIssue]:
        """Sync issues by external IDs."""
        if not external_ids:
            return []

        jql = f"project = {self.project_key} AND 'External ID' in ({','.join(f'\"{id}\"' for id in external_ids)})"
        return self.search_issues(jql)

    def get_transitions(self, issue_key: str) -> List[Dict]:
        """Get available transitions for an issue."""
        return self._make_request("GET", f"issue/{issue_key}/transitions")

    def transition_issue(self, issue_key: str, transition_id: str) -> JiraIssue:
        """Transition an issue to a new status."""
        payload = {"transition": {"id": transition_id}}
        data = self._make_request("POST", f"issue/{issue_key}/transitions", json=payload)
        return JiraIssue(**data)

class JiraClientError(Exception):
    """Custom exception for Jira client errors."""
    pass

# Example usage
if __name__ == "__main__":
    # Load from environment or provide config directly
    client = JiraClient()

    try:
        # Example: Get an issue
        issue = client.get_issue("PROJ-123")
        print(f"Got issue: {issue.key} - {issue.title}")

        # Example: Search for issues
        issues = client.search_issues("project = PROJ AND status = 'In Progress'")
        print(f"Found {len(issues)} issues in progress")

    except JiraClientError as e:
        print(f"Error: {e}")

