


"""
Data transfer objects for integration API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class IntegrationConfig(BaseModel):
    """Base configuration for integrations."""
    service: str  # "jira" or "trello"
    enabled: bool = True
    sync_interval: int = 3600  # Default: 1 hour

class JiraConfig(IntegrationConfig):
    """Configuration for Jira integration."""
    base_url: str
    username: str
    api_token: str
    project_key: str
    service: str = "jira"

class TrelloConfig(IntegrationConfig):
    """Configuration for Trello integration."""
    api_key: str
    api_token: str
    board_id: str
    service: str = "trello"

class SyncRequest(BaseModel):
    """Request model for sync operations."""
    service: str  # "jira" or "trello"
    task_ids: Optional[List[str]] = None  # Specific tasks to sync

class SyncResult(BaseModel):
    """Result model for sync operations."""
    status: str
    service: str
    synced_tasks: int
    message: Optional[str] = None
    errors: Optional[List[str]] = None

class ExternalTask(BaseModel):
    """Represents a task from external system."""
    external_id: str
    title: str
    status: str
    value: Optional[float] = None
    effort: Optional[float] = None
    last_sync: Optional[datetime] = None
    service: str  # "jira" or "trello"

class IntegrationStatus(BaseModel):
    """Status of integration services."""
    service: str
    connected: bool
    last_sync: Optional[datetime] = None
    next_sync: Optional[datetime] = None
    tasks_synced: int = 0

class CreateExternalTaskRequest(BaseModel):
    """Request to create task in external system."""
    task_id: str  # Local task ID
    service: str  # "jira" or "trello"
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None  # For Jira
    labels: Optional[List[str]] = None  # For Trello

class CreateExternalTaskResponse(BaseModel):
    """Response for task creation in external system."""
    status: str
    external_id: Optional[str] = None
    service: str
    message: Optional[str] = None

class IntegrationError(BaseModel):
    """Error information for integrations."""
    service: str
    error_type: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


