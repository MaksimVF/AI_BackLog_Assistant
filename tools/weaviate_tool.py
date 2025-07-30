




import os
import weaviate
from typing import Optional

# Временные параметры подключения (должны быть перемещены в settings.py)
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", None)

# Инициализация клиента
auth_config = None
if WEAVIATE_API_KEY:
    auth_config = weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY)

connection_params = weaviate.connect.ConnectionParams.from_url(WEAVIATE_URL, grpc_port=50051)
client = weaviate.WeaviateClient(
    connection_params=connection_params,
    auth_client_secret=auth_config
)

DEFAULT_CLASS_NAME = "AgentMemory"

def ensure_class_exists(class_name: str = DEFAULT_CLASS_NAME):
    """
    Создаёт схему в Weaviate, если она ещё не существует.
    """
    if not client.schema.contains({"class": class_name}):
        client.schema.create_class({
            "class": class_name,
            "vectorizer": "text2vec-openai",  # или другой векторизатор, если локальный
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"]
                },
                {
                    "name": "user_id",
                    "dataType": ["string"]
                }
            ]
        })

def store_document(text: str, user_id: str, class_name: str = DEFAULT_CLASS_NAME):
    """
    Сохраняет документ в память.
    """
    ensure_class_exists(class_name)
    client.data_object.create(
        data_object={"content": text, "user_id": user_id},
        class_name=class_name
    )

def semantic_search(query: str, user_id: Optional[str] = None, class_name: str = DEFAULT_CLASS_NAME, top_k: int = 5):
    """
    Выполняет семантический поиск по памяти.
    """
    filters = None
    if user_id:
        filters = {
            "path": ["user_id"],
            "operator": "Equal",
            "valueString": user_id
        }

    result = client.query.get(class_name, ["content", "user_id"])\
        .with_near_text({"concepts": [query]})\
        .with_where(filters)\
        .with_limit(top_k)\
        .do()

    return result["data"]["Get"].get(class_name, [])




