import weaviate
from typing import Optional, Dict, Any, List
import json

class WeaviateMemory:
    """Weaviate vector store client for memory management"""

    def __init__(self, url: str = "http://localhost:8080", scheme: str = "http"):
        self.client = weaviate.Client(url=url)
        self._setup_schema()

    def _setup_schema(self):
        """Set up the schema for our multi-agent system"""
        # Check if schema exists, if not create it
        if not self.client.schema.exists("Case"):
            case_class = {
                "class": "Case",
                "properties": [
                    {"name": "content", "dataType": ["string"]},
                    {"name": "context", "dataType": ["string"]},
                    {"name": "domain_tags", "dataType": ["string[]"]},
                    {"name": "metadata", "dataType": ["string"]},
                    {"name": "processing_status", "dataType": ["string"]},
                    {"name": "agents_involved", "dataType": ["string[]"]}
                ],
                "vectorizer": "text2vec-transformers"  # Using default vectorizer
            }
            self.client.schema.create_class(case_class)

    def store_case(self, case_id: str, content: str, context: str, domain_tags: List[str], metadata: Optional[Dict] = None) -> Dict:
        """Store a case in Weaviate"""
        case_data = {
            "content": content,
            "context": context,
            "domain_tags": domain_tags,
            "metadata": json.dumps(metadata) if metadata else "{}",
            "processing_status": "new",
            "agents_involved": []
        }

        return self.client.data_object.create(case_data, "Case", case_id)

    def update_case_status(self, case_id: str, status: str, agents: List[str]) -> Dict:
        """Update case processing status and agents involved"""
        updates = {
            "processing_status": status,
            "agents_involved": agents
        }

        return self.client.data_object.update(case_id, "Case", updates)

    def find_similar_case(self, text: str) -> Optional[str]:
        """
        Find similar case in Weaviate

        Args:
            text: Input text to search for

        Returns:
            ID of similar case if found, None otherwise
        """
        response = self.client.query.get("Case", ["id"]).with_near_text({"concepts": [text]}).with_limit(1).do()

        if response.get("data", {}).get("Get", {}).get("Case"):
            return response["data"]["Get"]["Case"][0]["id"]

        return None

    def query_similar_cases(self, text: str, limit: int = 3) -> List[Dict]:
        """
        Query similar cases from Weaviate

        Args:
            text: Input text to search for
            limit: Maximum number of results to return

        Returns:
            List of similar cases
        """
        response = self.client.query.get("Case", ["id", "content", "context", "domain_tags"]).with_near_text({"concepts": [text]}).with_limit(limit).do()

        cases = []
        if response.get("data", {}).get("Get", {}).get("Case"):
            for case in response["data"]["Get"]["Case"]:
                cases.append({
                    "id": case["id"],
                    "content": case.get("content", ""),
                    "context": case.get("context", ""),
                    "domain_tags": case.get("domain_tags", [])
                })

        return cases
