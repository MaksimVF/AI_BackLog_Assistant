# tools/transcribe_audio.py

from crewai_tools import BaseTool

class TranscribeAudioTool(BaseTool):
    name = "transcribe_audio"
    description = "Преобразует аудио в текст с использованием модели Whisper"

    def _run(self, audio_file_path: str) -> str:
        # TODO: Implement using whisper.cpp or faster-whisper
        return "Реализация будет добавлена позже"
