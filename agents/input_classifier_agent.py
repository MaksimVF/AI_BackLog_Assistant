


from crewai import Agent
from tools.file_type_detector import FileTypeDetectorTool
from tools.transcribe_audio import AudioTranscriptionTool
from tools.run_ocr import OCRTool
from tools.extract_audio_from_video import AudioExtractorTool

file_type_detector = FileTypeDetectorTool()
audio_transcriber = AudioTranscriptionTool()
ocr_tool = OCRTool()
audio_extractor = AudioExtractorTool()

InputClassifierAgent = Agent(
    role="Классификатор входной информации",
    goal="Определять тип входных данных и вызывать соответствующие инструменты обработки",
    tools=[
        file_type_detector,
        audio_transcriber,
        ocr_tool,
        audio_extractor
    ],
    verbose=True,
    allow_delegation=True
)


