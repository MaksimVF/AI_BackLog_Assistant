import os
import weaviate
from config import settings
from weaviate.schema_config import init_weaviate

class WeaviateStorageTool:
    def __init__(self):
        self.client = init_weaviate(settings.WEAVIATE_URL)

    def store_chunk(self, content, source_type, source_name, metadata=None):
        if metadata is None:
            metadata = {}

        # Создаём объект для Weaviate
        chunk_data = {
            "content": content,
            "source_type": source_type,
            "source_name": source_name,
            "metadata": metadata
        }

        # Сохраняем в Weaviate
        self.client.data_object.create(
            data_object=chunk_data,
            class_name="DocumentChunk"
        )

        return {"status": "stored", "content_length": len(content)}

    def query_chunks(self, query, limit=5):
        # Поиск по контенту
        result = self.client.query.get(
            class_name="DocumentChunk",
            properties=["content", "source_type", "source_name", "metadata"]
        ).with_where({
            "path": ["content"],
            "operator": "Like",
            "valueText": f"*{query}*"
        }).with_limit(limit).do()

        return result["data"]["Get"]["DocumentChunk"]

    def semantic_search(self, query, limit=5):
        # Семантический поиск
        result = self.client.query.get(
            class_name="DocumentChunk",
            properties=["content", "source_type", "source_name", "metadata"]
        ).with_near_text({
            "concepts": [query]
        }).with_limit(limit).do()

        return result["data"]["Get"]["DocumentChunk"]
