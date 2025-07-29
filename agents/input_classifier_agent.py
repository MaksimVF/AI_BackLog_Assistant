from crewai import Agent
from tools.file_type_detector import FileTypeDetectorTool
from tools.transcribe_audio import AudioTranscriptionTool
from tools.run_ocr import OCRTool

file_type_detector = FileTypeDetectorTool()
audio_transcriber = AudioTranscriptionTool()
ocr_tool = OCRTool()

InputClassifierAgent = Agent(
    role="Классификатор входной информации",
    goal="Определять тип входных данных и вызывать соответствующие инструменты обработки",
    tools=[
        file_type_detector,
        audio_transcriber,
        ocr_tool
    ],
    verbose=True,
    allow_delegation=True
)
