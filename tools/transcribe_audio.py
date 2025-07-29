from crewai_tools import BaseTool
from faster_whisper import WhisperModel

class AudioTranscriptionTool(BaseTool):
    name = "transcribe_audio"
    description = "Преобразует аудиофайл в текст (Speech-to-Text)"

    def _run(self, audio_path: str) -> str:
        model_size = "base"  # можно заменить на "small", "medium" и т.д.
        model = WhisperModel(model_size, compute_type="int8")

        segments, info = model.transcribe(audio_path)
        transcript = ""

        for segment in segments:
            transcript += f"{segment.text.strip()} "

        return transcript.strip()
