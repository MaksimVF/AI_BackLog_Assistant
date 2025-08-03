

"""
Input Processing Pipeline (IPP)

Coordinates the flow of data through input processing agents:
1. ModalityDetectorAgent
2. TextProcessorAgent / AudioTranscriberAgent / VideoAnalyzerAgent
3. EntityExtractor
4. IntentIdentifier
5. MetadataBuilder

Input: Raw user input (text, audio, video)
Output: Structured input with basic metadata
"""

from typing import Dict, Any
from pydantic import BaseModel, validator
from agents.modality_detector_agent import modality_detector_agent
from agents.text_processor_agent import text_processor_agent
from agents.audio_transcriber_agent import audio_transcriber_agent
from agents.video_analyzer_agent import video_analyzer_agent
from agents.analyzers.entity_extractor import EntityExtractor
from agents.analyzers.intent_identifier import IntentIdentifier
from agents.analyzers.metadata_builder import MetadataBuilder
from tools.document_processor import extract_document_content
from .base_pipeline import BasePipeline, PipelineConfig

class IPPInputSchema(BaseModel):
    """Input schema for IPP"""
    document_id: str
    raw_content: Any  # Can be text, audio, video data
    metadata: Dict[str, Any] = {}

    @validator('document_id')
    def document_id_not_empty(cls, v):
        if not v:
            raise ValueError("document_id cannot be empty")
        return v

class IPPOutputSchema(BaseModel):
    """Output schema for IPP"""
    document_id: str
    raw_text: str
    modality: str
    entities: Dict[str, Any]
    intent: str
    metadata: Dict[str, Any]

    @validator('modality')
    def valid_modality(cls, v):
        valid_modalities = ['text', 'audio', 'video', 'image', 'document']
        if v not in valid_modalities:
            raise ValueError(f"Invalid modality: {v}. Must be one of {valid_modalities}")
        return v

class InputProcessingPipeline(BasePipeline):
    """
    Input Processing Pipeline Coordinator
    """

    def __init__(self, config: PipelineConfig = None):
        super().__init__(config)
        self.modality_detector = modality_detector_agent
        self.text_processor = text_processor_agent
        self.audio_transcriber = audio_transcriber_agent
        self.video_analyzer = video_analyzer_agent
        self.entity_extractor = EntityExtractor()
        self.intent_identifier = IntentIdentifier()
        self.metadata_builder = MetadataBuilder()

    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data against IPPInputSchema"""
        try:
            validated = IPPInputSchema(**data).dict()
            return validated
        except Exception as e:
            self._log(f"Input validation failed: {e}", "error")
            raise

    def _validate_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate output data against IPPOutputSchema"""
        try:
            validated = IPPOutputSchema(**data).dict()
            return validated
        except Exception as e:
            self._log(f"Output validation failed: {e}", "error")
            raise

    def _process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the IPP pipeline.

        Steps:
        1. Detect modality
        2. Process based on modality (text/audio/video)
        3. Extract entities
        4. Identify intent
        5. Build metadata
        """
        document_id = data['document_id']
        raw_content = data['raw_content']
        input_metadata = data.get('metadata', {})

        # Step 1: Detect modality
        self._log(f"Processing document {document_id}: Detecting modality")
        modality = self._detect_modality(raw_content)

        # Step 2: Process based on modality
        self._log(f"Processing document {document_id}: Processing {modality} content")
        if modality == 'text':
            processed_text = self._process_text(raw_content)
        elif modality == 'audio':
            processed_text = self._process_audio(raw_content)
        elif modality == 'video':
            processed_text = self._process_video(raw_content)
        elif modality == 'document':
            processed_text = self._process_document(raw_content)
        else:
            processed_text = str(raw_content)  # Fallback for unknown modalities

        # Step 3: Extract entities
        self._log(f"Processing document {document_id}: Extracting entities")
        entities = self.entity_extractor.extract(processed_text)

        # Step 4: Identify intent
        self._log(f"Processing document {document_id}: Identifying intent")
        intent_analysis = self.intent_identifier.identify(processed_text)
        intent = intent_analysis.intent_type

        # Step 5: Build metadata
        self._log(f"Processing document {document_id}: Building metadata")
        metadata = self.metadata_builder.build(
            document_id=document_id,
            modality=modality,
            intent=intent,
            entities=entities,
            input_metadata=input_metadata
        )

        return {
            'document_id': document_id,
            'raw_text': processed_text,
            'modality': modality,
            'entities': entities,
            'intent': intent,
            'metadata': metadata
        }

    def _detect_modality(self, content: Any) -> str:
        """Detect the modality of the input content"""
        # This would be implemented by calling the modality detector agent
        # For now, return a placeholder based on content type
        if isinstance(content, str):
            # Check if the content is a file path
            if content.endswith('.pdf') or content.endswith('.docx') or content.endswith('.txt') or content.endswith('.csv'):
                return 'document'
            return 'text'
        elif hasattr(content, 'read'):  # File-like object
            # In a real implementation, we'd analyze the file content
            return 'document'  # Assume it's a document file
        else:
            return 'text'  # Default fallback

    def _process_text(self, text_content: str) -> str:
        """Process text content"""
        # This would call the text processor agent
        # For now, return the text as-is
        return text_content

    def _process_audio(self, audio_content: Any) -> str:
        """Process audio content"""
        # This would call the audio transcriber agent
        # For now, return a placeholder
        return "Transcribed text from audio"

    def _process_video(self, video_content: Any) -> str:
        """Process video content"""
        # This would call the video analyzer agent
        # For now, return a placeholder
        return "Extracted text from video"

    def _process_document(self, document_path: str) -> str:
        """Process document file content"""
        # Extract text from the document using the document processor
        try:
            return extract_document_content(document_path)
        except Exception as e:
            self._log(f"Error processing document {document_path}: {e}", "error")
            return f"Error processing document: {e}"

