



from crewai_tools import BaseTool
from moviepy.editor import VideoFileClip
import whisper
import os
import tempfile

class VideoToTextTool(BaseTool):
    name = "video_to_text_tool"
    description = "Извлекает аудио из видеофайла и конвертирует его в текст с помощью модели Whisper."

    def _execute(self, video_path: str) -> str:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Видео не найдено: {video_path}")

        try:
            # Извлечение аудио во временный файл
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
                video = VideoFileClip(video_path)
                video.audio.write_audiofile(temp_audio.name, codec='libmp3lame')
                audio_path = temp_audio.name

            # Загрузка модели Whisper и транскрибация
            model = whisper.load_model("base")  # Модель можно заменить на tiny, small, medium и т.д.
            result = model.transcribe(audio_path)

            # Удаление временного аудио
            os.remove(audio_path)

            return result["text"].strip()
        except Exception as e:
            return f"Ошибка при обработке видео: {str(e)}"



