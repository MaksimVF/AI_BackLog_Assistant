






import weaviate

def create_schema(client):
    if client.schema.exists("DocumentChunk"):
        return
    schema = {
        "classes": [
            {
                "class": "DocumentChunk",
                "description": "Сегмент текстовой информации, связанный с файлом",
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "source_type", "dataType": ["text"]},
                    {"name": "source_name", "dataType": ["text"]},
                    {"name": "timestamp", "dataType": ["date"]},
                    {"name": "metadata", "dataType": ["object"]},
                ],
            }
        ]
    }
    client.schema.create(schema)

def init_weaviate(weaviate_url="http://weaviate:8080"):
    client = weaviate.Client(weaviate_url)
    create_schema(client)
    return client






