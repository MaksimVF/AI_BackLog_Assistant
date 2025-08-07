

import os
from pathlib import Path
from dotenv import load_dotenv
from .advanced_config import config

# Загрузка переменных окружения
load_dotenv()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Пути к данным (локальные)
DATA_PATH = BASE_DIR / "data"
VIDEO_PATH = DATA_PATH / "videos"
AUDIO_PATH = DATA_PATH / "audios"
TRANSCRIPTS_PATH = DATA_PATH / "transcripts"

# Убедимся, что директории существуют
for path in [DATA_PATH, VIDEO_PATH, AUDIO_PATH, TRANSCRIPTS_PATH]:
    path.mkdir(parents=True, exist_ok=True)

# Redis
REDIS_URL = config.config.redis.url

# Weaviate
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")

# Для future use: API ключи, креденшелы и прочее
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# Общее логирование
LOG_PATH = BASE_DIR / "logs"
LOG_PATH.mkdir(exist_ok=True)

# Логирование
LOG_LEVEL = config.config.log_level

# Очереди
QUEUE_NAMES = {
    "video": "video_processing",
    "image": "image_processing",
    "transcription": "transcription"
}

# NLP и эмбеддинги
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "intfloat/multilingual-e5-small")

# Security settings
SECRET_KEY = config.config.security.secret_key
ALGORITHM = config.config.security.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.config.security.access_token_expire_minutes

# SSL/TLS settings
SSL_CERTIFICATE = os.getenv("SSL_CERTIFICATE", "cert.pem")
SSL_KEY = os.getenv("SSL_KEY", "key.pem")

