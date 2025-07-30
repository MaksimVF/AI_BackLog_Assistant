



import requests
from typing import List, Dict, Optional

class WeaviateTool:
    def __init__(self, weaviate_url: str = "http://localhost:8081"):
        self.weaviate_url = weaviate_url.rstrip("/")
        self.collection = "DocumentChunk"

    def add_document_chunk(
        self,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict] = None,
    ) -> bool:
        """
        Добавляет фрагмент документа в Weaviate.
        """
        url = f"{self.weaviate_url}/v1/objects"
        payload = {
            "class": self.collection,
            "properties": {
                "text": text,
                **(metadata or {})
            },
            "vector": embedding,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"[ERROR] Weaviate insert failed: {e}")
            return False

    def search_similar_chunks(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Выполняет семантический поиск по эмбеддингу.
        """
        url = f"{self.weaviate_url}/v1/graphql"
        query = {
            "query": f"""
            {{
              Get {{
                {self.collection}(
                  nearVector: {{
                    vector: {embedding},
                    certainty: 0.7
                  }},
                  limit: {top_k}
                ) {{
                  text
                  _additional {{
                    distance
                  }}
                }}
              }}
            }}
            """
        }

        try:
            response = requests.post(url, json=query)
            response.raise_for_status()
            return response.json()["data"]["Get"][self.collection]
        except requests.RequestException as e:
            print(f"[ERROR] Weaviate search failed: {e}")
            return []

if __name__ == "__main__":
    from semantic_embedder import SemanticEmbedder

    embedder = SemanticEmbedder()
    weaviate = WeaviateTool()

    text = "Пример содержимого для сохранения в базу знаний"
    embedding = embedder.embed(text)

    if embedding:
        weaviate.add_document_chunk(text, embedding, metadata={"source": "manual"})

        results = weaviate.search_similar_chunks(embedding)
        for r in results:
            print(f"→ {r['text']} (distance: {r['_additional']['distance']})")




