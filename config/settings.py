








import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Weaviate
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Пути
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/uploads")
PROCESSED_DIR = os.getenv("PROCESSED_DIR", "/tmp/processed")

# Токены и ключи
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# Логирование
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Очереди
QUEUE_NAMES = {
    "video": "video_processing",
    "image": "image_processing",
    "transcription": "transcription"
}









