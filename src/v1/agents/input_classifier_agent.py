from crewai import Agent
from tools.file_type_detector import FileTypeDetectorTool
from tools.transcribe_audio import AudioTranscriptionTool
from tools.run_ocr import OCRTool
from tools.extract_audio_from_video import AudioExtractorTool
from tools.audio2text_tool import AudioToTextTool
from tools.image2text_tool import ImageToTextTool
from tools.video2text_tool import VideoToTextTool
from tools.video_frame_extractor_tool import VideoFrameExtractorTool
from tools.weaviate_storage_tool import WeaviateStorageTool

file_type_detector = FileTypeDetectorTool()
audio_transcriber = AudioTranscriptionTool()
ocr_tool = OCRTool()
audio_extractor = AudioExtractorTool()
audio_to_text = AudioToTextTool()
image_to_text = ImageToTextTool()
video_to_text = VideoToTextTool()
frame_extractor = VideoFrameExtractorTool()
weaviate_storage = WeaviateStorageTool()

InputClassifierAgent = Agent(
    role="Классификатор входной информации",
    goal="Определять тип входных данных и вызывать соответствующие инструменты обработки",
    tools=[
        file_type_detector,
        audio_transcriber,
        ocr_tool,
        audio_extractor,
        audio_to_text,
        image_to_text,
        video_to_text,
        frame_extractor,
        weaviate_storage
    ],
    verbose=True,
    allow_delegation=True
)
