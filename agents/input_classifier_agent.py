


from crewai import Agent
from tools.file_type_detector import FileTypeDetectorTool
from tools.transcribe_audio import AudioTranscriptionTool
from tools.run_ocr import OCRTool
from tools.extract_audio_from_video import AudioExtractorTool
from tools.audio2text_tool import AudioToTextTool

file_type_detector = FileTypeDetectorTool()
audio_transcriber = AudioTranscriptionTool()
ocr_tool = OCRTool()
audio_extractor = AudioExtractorTool()
audio_to_text = AudioToTextTool()

InputClassifierAgent = Agent(
    role="Классификатор входной информации",
    goal="Определять тип входных данных и вызывать соответствующие инструменты обработки",
    tools=[
        file_type_detector,
        audio_transcriber,
        ocr_tool,
        audio_extractor,
        audio_to_text
    ],
    verbose=True,
    allow_delegation=True
)


