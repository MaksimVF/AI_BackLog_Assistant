




"""
Level 1 Processing Pipeline
"""

import logging
from typing import Dict, Any
from src.v2.agents.level1.input_receiver import InputReceiverAgent, InputData
from src.v2.agents.level1.modality_detector import ModalityDetectionAgent
from src.v2.agents.level1.processors.text_processor import TextProcessor
from src.v2.agents.level1.processors.audio_transcriber import AudioTranscriber
from src.v2.agents.level1.processors.video_processor import VideoProcessor
from src.v2.agents.level1.processors.image_processor import ImageProcessor
from src.v2.agents.level1.content_classifier import ContentClassifierAgent
from src.v2.agents.level1.trigger_agent import TriggerAgent

logger = logging.getLogger(__name__)

class Level1Pipeline:
    """Coordinates Level 1 processing"""

    def __init__(self):
        # Initialize agents
        self.input_receiver = InputReceiverAgent()
        self.modality_detector = ModalityDetectionAgent()
        self.processors = {
            'text': TextProcessor(),
            'audio': AudioTranscriber(),
            'video': VideoProcessor(),
            'image': ImageProcessor()
        }
        self.content_classifier = ContentClassifierAgent()
        self.trigger_agent = TriggerAgent()

    def process(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input through Level 1 pipeline

        Args:
            raw_input: Raw input data

        Returns:
            Processed data with classification and trigger information
        """
        try:
            # Step 1: Receive and validate input
            logger.info("Step 1: Receiving input")
            input_data = self.input_receiver.receive(raw_input)

            # Step 2: Detect modality
            logger.info("Step 2: Detecting modality")
            modality = self.modality_detector.detect(input_data)

            # Step 3: Process based on modality
            logger.info(f"Step 3: Processing {modality} data")
            processor = self.processors.get(modality)
            if not processor:
                raise ValueError(f"Unsupported modality: {modality}")

            processed_data = processor.process(input_data)

            # Step 4: Classify content
            logger.info("Step 4: Classifying content")
            classified_data = self.content_classifier.classify(processed_data)

            # Step 5: Check trigger conditions
            logger.info("Step 5: Checking trigger conditions")
            should_trigger = self.trigger_agent.check_conditions(classified_data)

            result = {
                'processed_data': classified_data,
                'trigger_level2': should_trigger,
                'modality': modality
            }

            logger.info(f"Level 1 processing complete. Trigger Level 2: {should_trigger}")
            return result

        except Exception as e:
            logger.error(f"Level 1 pipeline failed: {e}")
            raise ValueError(f"Level 1 processing failed: {e}")

    def manual_trigger(self) -> bool:
        """Manually trigger Level 2 processing"""
        return self.trigger_agent.manual_trigger()

    def update_trigger_thresholds(self, thresholds: Dict[str, Any]) -> None:
        """Update trigger thresholds"""
        self.trigger_agent.update_thresholds(thresholds)





