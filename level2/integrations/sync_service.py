


"""
Sync Service for integrating with external task management systems.
"""

from typing import List, Dict, Optional, Union, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .jira_client import JiraClient, JiraIssue, JiraConfig
from .trello_client import TrelloClient, TrelloCard, TrelloConfig

# Import Task model directly
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.models_second_level import Task
from db.session import get_async_session

class SyncService:
    """
    Service for syncing tasks between local database and external systems.

    Features:
    - Bidirectional sync with Jira and Trello
    - Conflict resolution
    - Task mapping and transformation
    - Error handling and logging
    """

    def __init__(self):
        """Initialize sync service with clients."""
        self.jira_client = JiraClient()
        self.trello_client = TrelloClient()

    async def sync_with_jira(self, session: AsyncSession, project_key: Optional[str] = None) -> Dict:
        """Sync tasks with Jira."""
        try:
            # Get all tasks from local DB that have Jira external IDs
            result = await session.execute(
                select(Task).where(Task.external_id != None)
            )
            local_tasks = result.scalars().all()

            # Extract Jira external IDs
            jira_ids = [task.external_id for task in local_tasks if task.external_id.startswith("jira:")]

            if not jira_ids:
                return {"status": "success", "synced": 0, "message": "No Jira tasks to sync"}

            # Sync with Jira
            jira_issues = self.jira_client.sync_issues([id.replace("jira:", "") for id in jira_ids])

            # Update local tasks with Jira data
            for issue in jira_issues:
                local_task = next((t for t in local_tasks if t.external_id == f"jira:{issue.key}"), None)
                if local_task:
                    await self._update_task_from_jira(local_task, issue, session)

            return {"status": "success", "synced": len(jira_issues)}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def sync_with_trello(self, session: AsyncSession) -> Dict:
        """Sync tasks with Trello."""
        try:
            # Get all tasks from local DB that have Trello external IDs
            result = await session.execute(
                select(Task).where(Task.external_id != None)
            )
            local_tasks = result.scalars().all()

            # Extract Trello external IDs
            trello_ids = [task.external_id for task in local_tasks if task.external_id.startswith("trello:")]

            if not trello_ids:
                return {"status": "success", "synced": 0, "message": "No Trello tasks to sync"}

            # Sync with Trello
            trello_cards = self.trello_client.sync_cards([id.replace("trello:", "") for id in trello_ids])

            # Update local tasks with Trello data
            for card in trello_cards:
                local_task = next((t for t in local_tasks if t.external_id == f"trello:{card.id}"), None)
                if local_task:
                    await self._update_task_from_trello(local_task, card, session)

            return {"status": "success", "synced": len(trello_cards)}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _update_task_from_jira(self, task: Task, issue: JiraIssue, session: AsyncSession):
        """Update local task from Jira issue."""
        task.title = issue.title
        task.status = issue.status
        task.value = self._map_priority_to_value(issue.priority)
        task.effort = self._estimate_effort(issue)
        task.updated_at = issue.updated_at

        session.add(task)
        await session.commit()

    async def _update_task_from_trello(self, task: Task, card: TrelloCard, session: AsyncSession):
        """Update local task from Trello card."""
        task.title = card.name
        task.status = self._map_trello_status(card.status)
        task.value = self._map_labels_to_value(card.labels)
        task.effort = self._estimate_effort_from_card(card)
        task.updated_at = card.updated_at

        session.add(task)
        await session.commit()

    def _map_priority_to_value(self, priority: str) -> float:
        """Map Jira priority to value score."""
        priority_map = {
            "Highest": 10.0,
            "High": 7.5,
            "Medium": 5.0,
            "Low": 2.5,
            "Lowest": 1.0
        }
        return priority_map.get(priority, 5.0)

    def _map_trello_status(self, list_id: str) -> str:
        """Map Trello list ID to status."""
        # This would be configured based on the specific board
        status_map = {
            "list_1": "planned",
            "list_2": "in_progress",
            "list_3": "completed"
        }
        return status_map.get(list_id, "planned")

    def _map_labels_to_value(self, labels: List[str]) -> float:
        """Map Trello labels to value score."""
        value = 5.0  # default
        for label in labels:
            if "high" in label.lower():
                value = 8.0
            elif "medium" in label.lower():
                value = 5.0
            elif "low" in label.lower():
                value = 2.0
        return value

    def _estimate_effort(self, issue: JiraIssue) -> float:
        """Estimate effort from Jira issue."""
        # Simple estimation based on priority and description length
        priority_effort = {
            "Highest": 10.0,
            "High": 7.0,
            "Medium": 5.0,
            "Low": 3.0,
            "Lowest": 1.0
        }

        base_effort = priority_effort.get(issue.priority, 5.0)
        description_factor = min(len(issue.description or "") / 100, 2.0)  # Max 2x multiplier

        return base_effort * description_factor

    def _estimate_effort_from_card(self, card: Optional[TrelloCard] = None) -> float:
        """Estimate effort from Trello card."""
        # Simple estimation based on labels and description length
        base_effort = 5.0

        if card and hasattr(card, 'labels') and card.labels:
            for label in card.labels:
                if "complex" in label.lower():
                    base_effort = 8.0
                elif "simple" in label.lower():
                    base_effort = 3.0

        description_length = len(card.desc or "") if card else 0
        description_factor = min(description_length / 100, 2.0)  # Max 2x multiplier

        return base_effort * description_factor

    async def create_jira_task(self, task: Task, session: AsyncSession) -> JiraIssue:
        """Create a new task in Jira."""
        try:
            issue = self.jira_client.create_issue(
                title=task.title,
                description=task.title,  # Use title as description if none
                priority=self._map_value_to_priority(task.value),
                # Add custom field for external ID
                **{"customfield_12345": task.id}  # Replace with actual custom field ID
            )

            # Update local task with Jira reference
            task.external_id = f"jira:{issue.key}"
            session.add(task)
            await session.commit()

            return issue

        except Exception as e:
            raise SyncServiceError(f"Failed to create Jira task: {str(e)}") from e

    async def create_trello_task(self, task: Task, session: AsyncSession) -> TrelloCard:
        """Create a new task in Trello."""
        try:
            # Get default list ID (e.g., "To Do" column)
            lists = self.trello_client.get_lists()
            default_list = lists[0]["id"] if lists else None

            if not default_list:
                raise SyncServiceError("No lists found in Trello board")

            card = self.trello_client.create_card(
                name=task.title,
                list_id=default_list,
                desc=task.title,  # Use title as description if none
                labels=self._map_value_to_labels(task.value)
            )

            # Update local task with Trello reference
            task.external_id = f"trello:{card.id}"
            session.add(task)
            await session.commit()

            return card

        except Exception as e:
            raise SyncServiceError(f"Failed to create Trello task: {str(e)}") from e

    def _map_value_to_priority(self, value: float) -> str:
        """Map value score to Jira priority."""
        if value > 8.0:
            return "Highest"
        elif value > 6.0:
            return "High"
        elif value > 3.0:
            return "Medium"
        elif value > 1.0:
            return "Low"
        else:
            return "Lowest"

    def _map_value_to_labels(self, value: float) -> List[str]:
        """Map value score to Trello labels."""
        labels = []
        if value > 8.0:
            labels.append("High Priority")
        elif value > 6.0:
            labels.append("Medium Priority")
        elif value > 3.0:
            labels.append("Low Priority")
        return labels

class SyncServiceError(Exception):
    """Custom exception for sync service errors."""
    pass

# Example usage
async def example_sync():
    """Example of how to use the sync service."""
    async for session in get_async_session():
        sync_service = SyncService()

        # Sync with Jira
        jira_result = await sync_service.sync_with_jira(session)
        print(f"Jira sync result: {jira_result}")

        # Sync with Trello
        trello_result = await sync_service.sync_with_trello(session)
        print(f"Trello sync result: {trello_result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_sync())

