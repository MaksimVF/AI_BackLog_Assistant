import weaviate
from typing import Optional, Dict, Any, List
import json
from utils.error_handling import AIBacklogError, DependencyError, handle_exception, ErrorSeverity

class WeaviateMemory:
    """Weaviate vector store client for memory management"""

    def __init__(self, url: str = "http://localhost:8080", scheme: str = "http"):
        try:
            # Try new Weaviate client API (v4+)
            self.client = weaviate.connect(url=url)
            self._setup_schema()
        except (ImportError, AttributeError):
            try:
                # Try old Weaviate client API (v3)
                self.client = weaviate.Client(url=url)
                self._setup_schema()
            except Exception as e:
                error = DependencyError(
                    f"Could not connect to Weaviate: {str(e)}",
                    service="weaviate",
                    context={"url": url, "scheme": scheme}
                )
                self.client = None

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

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the Weaviate instance.

        Returns:
            Dictionary with statistics including:
            - object_count: Total number of objects
            - class_count: Number of classes
            - schema_info: Schema details
        """
        if not self.client:
            return {
                "error": "Weaviate client not available",
                "object_count": 0,
                "class_count": 0,
                "schema_info": {}
            }

        try:
            # Get schema information
            schema = self.client.schema.get()
            classes = schema.get("classes", [])

            # Get object count
            object_count = 0
            for class_obj in classes:
                class_name = class_obj.get("class", "")
                try:
                    count_response = self.client.query.aggregate(class_name).with_meta_count().do()
                    class_count = count_response.get("data", {}).get("Aggregate", {}).get(class_name, [{}])[0].get("meta", {}).get("count", 0)
                    object_count += class_count
                except Exception as e:
                    log_error(
                    f"Could not get count for class {class_name}: {str(e)}",
                    severity=ErrorSeverity.WARNING,
                    error_code="AIBA_WEAVIATE_COUNT_ERROR",
                    context={"class_name": class_name}
                )

            return {
                "object_count": object_count,
                "class_count": len(classes),
                "schema_info": {
                    "classes": [c.get("class", "") for c in classes],
                    "properties": {c.get("class", ""): [p.get("name", "") for p in c.get("properties", [])] for c in classes}
                }
            }
        except Exception as e:
            error = handle_exception(
                    e,
                    severity=ErrorSeverity.ERROR,
                    error_code="AIBA_WEAVIATE_STATS_ERROR",
                    context={"method": "get_statistics"}
                )
            return {
                "error": str(e),
                "object_count": 0,
                "class_count": 0,
                "schema_info": {}
            }

    def get_case_statistics(self) -> Dict[str, Any]:
        """
        Get statistics specifically for Case objects.

        Returns:
            Dictionary with Case statistics including:
            - total_cases: Total number of cases
            - status_distribution: Count by processing status
            - domain_distribution: Count by domain tags
        """
        if not self.client:
            return {
                "error": "Weaviate client not available",
                "total_cases": 0,
                "status_distribution": {},
                "domain_distribution": {}
            }

        try:
            # Get total count
            count_response = self.client.query.aggregate("Case").with_meta_count().do()
            total_cases = count_response.get("data", {}).get("Aggregate", {}).get("Case", [{}])[0].get("meta", {}).get("count", 0)

            # Get status distribution
            status_response = self.client.query.aggregate("Case") \
                .with_fields("processing_status") \
                .with_group_by_filter(["processing_status"]) \
                .do()

            status_dist = {}
            for group in status_response.get("data", {}).get("Aggregate", {}).get("Case", []):
                status = group.get("groupedBy", {}).get("value", "unknown")
                count = group.get("meta", {}).get("count", 0)
                status_dist[status] = count

            # Get domain distribution
            domain_response = self.client.query.aggregate("Case") \
                .with_fields("domain_tags") \
                .with_group_by_filter(["domain_tags"]) \
                .do()

            domain_dist = {}
            for group in domain_response.get("data", {}).get("Aggregate", {}).get("Case", []):
                domain = group.get("groupedBy", {}).get("value", "unknown")
                count = group.get("meta", {}).get("count", 0)
                domain_dist[domain] = count

            return {
                "total_cases": total_cases,
                "status_distribution": status_dist,
                "domain_distribution": domain_dist
            }
        except Exception as e:
            error = handle_exception(
                    e,
                    severity=ErrorSeverity.ERROR,
                    error_code="AIBA_WEAVIATE_CASE_STATS_ERROR",
                    context={"method": "get_case_statistics"}
                )
            return {
                "error": str(e),
                "total_cases": 0,
                "status_distribution": {},
                "domain_distribution": {}
            }

