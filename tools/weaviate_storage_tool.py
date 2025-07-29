




import weaviate
import uuid
import datetime

class WeaviateStorageTool:
    def __init__(self, weaviate_url="http://weaviate:8080"):
        self.client = weaviate.Client(weaviate_url)

    def store_chunk(self, content, source_type, source_name, metadata=None):
        data_object = {
            "content": content,
            "source_type": source_type,
            "source_name": source_name,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        self.client.data_object.create(
            data_object=data_object,
            class_name="DocumentChunk",
            uuid=str(uuid.uuid4())
        )

    def query_chunks(self, query_text, limit=10):
        near_text = {"concepts": [query_text]}
        result = self.client.query.get("DocumentChunk", ["content", "source_type", "source_name"]).with_near_text(near_text).with_limit(limit).do()
        return result["data"]["Get"]["DocumentChunk"]




