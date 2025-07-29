import weaviate
from config import settings

def create_schema():
    schema = {
        "classes": [
            {
                "class": "DocumentChunk",
                "description": "Часть документа или медиафайла",
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "Текстовое содержимое фрагмента"
                    },
                    {
                        "name": "source_type",
                        "dataType": ["string"],
                        "description": "Тип источника (video, audio, image, text)"
                    },
                    {
                        "name": "source_name",
                        "dataType": ["string"],
                        "description": "Имя исходного файла"
                    },
                    {
                        "name": "timestamp",
                        "dataType": ["date"],
                        "description": "Время создания записи"
                    },
                    {
                        "name": "metadata",
                        "dataType": ["object"],
                        "description": "Дополнительные метаданные"
                    }
                ]
            }
        ]
    }
    return schema

def init_weaviate(weaviate_url):
    client = weaviate.Client(weaviate_url)

    # Проверяем, существует ли схема
    try:
        schema = client.schema.get()
        if "classes" not in schema or len(schema["classes"]) == 0:
            # Создаём схему, если она пустая
            client.schema.create(create_schema())
    except Exception as e:
        # Если ошибка, возможно, схема ещё не создана
        client.schema.create(create_schema())

    return client
