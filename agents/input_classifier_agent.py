from crewai import Agent
from tools.file_type_detector import FileTypeDetectorTool
from tools.transcribe_audio import AudioTranscriptionTool

file_type_detector = FileTypeDetectorTool()
audio_transcriber = AudioTranscriptionTool()

InputClassifierAgent = Agent(
    role="Классификатор входной информации",
    goal="Определять тип входных данных и вызывать соответствующие инструменты обработки",
    tools=[
        file_type_detector,
        audio_transcriber
    ],
    verbose=True,
    allow_delegation=True
)
