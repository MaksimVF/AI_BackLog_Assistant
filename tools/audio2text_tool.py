

from crewai_tools import BaseTool
from typing import Optional
import whisper
import os

class AudioToTextTool(BaseTool):
    name = "audio_to_text_tool"
    description = "Преобразует аудиофайл в текст с помощью модели Whisper. Поддерживает файлы .mp3, .wav, .m4a и другие."

    def __init__(self, model_size: str = "base"):
        super().__init__()
        self.model = whisper.load_model(model_size)

    def _execute(self, audio_path: str, language: Optional[str] = None) -> str:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Файл не найден: {audio_path}")

        try:
            result = self.model.transcribe(audio_path, language=language)
            return result["text"]
        except Exception as e:
            return f"Ошибка при обработке аудио: {str(e)}"

