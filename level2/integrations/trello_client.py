


"""
Trello Client for integrating with Trello API.
"""

import os
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
import requests
from pydantic import BaseModel, Field

class TrelloConfig(BaseModel):
    """Configuration for Trello client."""
    api_key: str
    api_token: str
    board_id: str

class TrelloCard(BaseModel):
    """Represents a Trello card."""
    id: str
    name: str
    desc: Optional[str]
    status: str = Field(alias="idList")  # List ID represents status/column
    labels: List[str] = []
    due: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    external_id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class TrelloClient:
    """
    Client for interacting with Trello API.

    Features:
    - Fetch cards from Trello boards
    - Create/update cards
    - Sync with local task database
    - Handle authentication
    """

    def __init__(self, config: Optional[TrelloConfig] = None):
        """
        Initialize Trello client.

        Args:
            config: Trello configuration. If None, will try to load from environment.
        """
        if config is None:
            config = self._load_config_from_env()

        self.config = config
        self.base_url = "https://api.trello.com/1"
        self.auth_params = {
            "key": config.api_key,
            "token": config.api_token
        }

    def _load_config_from_env(self) -> TrelloConfig:
        """Load configuration from environment variables."""
        return TrelloConfig(
            api_key=os.getenv("TRELLO_API_KEY", ""),
            api_token=os.getenv("TRELLO_API_TOKEN", ""),
            board_id=os.getenv("TRELLO_BOARD_ID", "")
        )

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make HTTP request to Trello API."""
        url = f"{self.base_url}/{endpoint}"

        # Merge auth params with any provided params
        params = {**self.auth_params, **(kwargs.get("params", {}))}
        kwargs["params"] = params

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            raise TrelloClientError(f"Trello API request failed: {str(e)}") from e

    def get_card(self, card_id: str) -> TrelloCard:
        """Get a single Trello card by ID."""
        data = self._make_request("GET", f"cards/{card_id}")
        return TrelloCard(**data)

    def get_cards_by_list(self, list_id: str) -> List[TrelloCard]:
        """Get all cards in a specific list."""
        data = self._make_request("GET", f"lists/{list_id}/cards")
        return [TrelloCard(**card) for card in data]

    def get_all_cards(self) -> List[TrelloCard]:
        """Get all cards from the configured board."""
        data = self._make_request("GET", f"boards/{self.config.board_id}/cards")
        return [TrelloCard(**card) for card in data]

    def create_card(self, name: str, list_id: str, description: str = "",
                   due: Optional[datetime] = None, labels: Optional[List[str]] = None) -> TrelloCard:
        """Create a new Trello card."""
        payload = {
            "name": name,
            "idList": list_id,
            "desc": description,
            "due": due.isoformat() if due else None,
            "labels": labels or []
        }

        data = self._make_request("POST", "cards", json=payload)
        return TrelloCard(**data)

    def update_card(self, card_id: str, **fields) -> TrelloCard:
        """Update an existing Trello card."""
        data = self._make_request("PUT", f"cards/{card_id}", json=fields)
        return TrelloCard(**data)

    def sync_cards(self, external_ids: List[str]) -> List[TrelloCard]:
        """Sync cards by external IDs."""
        if not external_ids:
            return []

        # Trello doesn't have a direct way to search by custom fields,
        # so we need to get all cards and filter
        all_cards = self.get_all_cards()
        return [card for card in all_cards if card.external_id in external_ids]

    def get_lists(self) -> List[Dict]:
        """Get all lists (columns) from the board."""
        return self._make_request("GET", f"boards/{self.config.board_id}/lists")

class TrelloClientError(Exception):
    """Custom exception for Trello client errors."""
    pass

# Example usage
if __name__ == "__main__":
    # Load from environment or provide config directly
    client = TrelloClient()

    try:
        # Example: Get a card
        card = client.get_card("card_id_here")
        print(f"Got card: {card.id} - {card.name}")

        # Example: Get all cards
        cards = client.get_all_cards()
        print(f"Found {len(cards)} cards on the board")

    except TrelloClientError as e:
        print(f"Error: {e}")


