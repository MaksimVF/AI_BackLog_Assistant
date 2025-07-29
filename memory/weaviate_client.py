

import weaviate
from typing import Optional, Dict, Any

class WeaviateMemory:
    """Weaviate vector store client for memory management"""

    def __init__(self, url: str = "http://localhost:8080", scheme: str = "http"):
        self.client = weaviate.Client(url=url)
        self._setup_schema()

    def _setup_schema(self):
        """Set up the schema for our multi-agent system"""
        # Check if schema exists, if not create it
        if not self.client.schema.exists("DataObject"):
            class_obj = {
                "class": "DataObject",
                "properties": [
                    {"name": "data_type", "dataType": ["string"]},
                    {"name": "content", "dataType": ["string"]},
                    {"name": "metadata", "dataType": ["string"]},
                    {"name": "processing_status", "dataType": ["string"]},
                    {"name": "agents_involved", "dataType": ["string[]"]}
                ],
                "vectorizer": "text2vec-transformers"  # Using default vectorizer
            }
            self.client.schema.create_class(class_obj)

    def store_data(self, data_id: str, data_type: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Store data in Weaviate"""
        data_object = {
            "data_type": data_type,
            "content": content,
            "metadata": str(metadata) if metadata else "",
            "processing_status": "new",
            "agents_involved": []
        }

        return self.client.data_object.create(data_object, "DataObject", data_id)

    def update_processing_status(self, data_id: str, status: str, agents: list) -> Dict:
        """Update processing status and agents involved"""
        updates = {
            "processing_status": status,
            "agents_involved": agents
        }

        return self.client.data_object.update(data_id, "DataObject", updates)

    def query_similar(self, query: str, limit: int = 5) -> list:
        """Query similar data objects"""
        near_text = {"concepts": [query]}
        return self.client.query.get("DataObject", ["data_type", "content"]).with_near_text(near_text).with_limit(limit).do()

