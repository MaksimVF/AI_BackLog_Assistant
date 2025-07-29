
from crewai_tools import BaseTool
import moviepy.editor as mp
import os

class AudioExtractorTool(BaseTool):
    name = "audio_extractor_tool"
    description = "Извлекает аудиодорожку из видеофайла и сохраняет её как .wav"

    def _run(self, video_path: str) -> str:
        try:
            video = mp.VideoFileClip(video_path)
            audio_path = video_path.rsplit(".", 1)[0] + ".wav"
            video.audio.write_audiofile(audio_path)
            return audio_path
        except Exception as e:
            return f"Ошибка при извлечении аудио: {str(e)}"
