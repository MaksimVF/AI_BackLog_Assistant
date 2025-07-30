



import requests
from typing import List, Optional


class SemanticEmbedder:
    def __init__(self, embedding_api_url: str = "http://localhost:8080/embed"):
        """
        :param embedding_api_url: URL локального или внешнего сервиса эмбеддинга (например, Ollama, vLLM или свой REST API).
        """
        self.embedding_api_url = embedding_api_url

    def embed(self, text: str) -> Optional[List[float]]:
        """
        Получает эмбеддинг одного текста.
        """
        try:
            response = requests.post(self.embedding_api_url, json={"text": text})
            response.raise_for_status()
            return response.json().get("embedding")
        except requests.RequestException as e:
            print(f"[ERROR] Embedding failed: {e}")
            return None

    def embed_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Получает эмбеддинги списка текстов.
        """
        return [self.embed(t) for t in texts]


if __name__ == "__main__":
    embedder = SemanticEmbedder("http://localhost:8080/embed")
    emb = embedder.embed("Пример текста для эмбеддинга")
    print(emb)



