



"""
Test script to demonstrate provider selection logic
"""

import logging
from src.common.utils import setup_logging
from src.v2.agents.level1.processors.audio_transcriber import AudioTranscriber
from src.v2.agents.level1.processors.image_processor import ImageProcessor
from src.v2.agents.level1.processors.video_processor import VideoProcessor
from src.v2.agents.level1.processors.text_processor import TextProcessor
from src.v2.agents.level1.input_receiver import InputData

def main():
    """Test provider selection logic"""
    # Set up logging
    setup_logging(log_level="INFO")

    logger = logging.getLogger("provider_test")
    logger.info("🧪 Testing Provider Selection Logic")

    # Create test inputs with different characteristics
    test_inputs = [
        {
            "content": "This is English text content",
            "source": "api",
            "metadata": {"language": "en", "content_type": "general"}
        },
        {
            "content": "Это русский текст",
            "source": "telegram",
            "metadata": {"language": "ru", "content_type": "social_media"}
        },
        {
            "content": "Este es texto en español",
            "source": "web",
            "metadata": {"language": "es", "content_type": "general"}
        },
        {
            "content": "这是中文文本",
            "source": "api",
            "metadata": {"language": "zh", "content_type": "document"}
        },
        {
            "content": "This is simulated audio content",
            "source": "api",
            "metadata": {"language": "en", "file_type": "audio/mp3"}
        },
        {
            "content": "This is simulated image content",
            "source": "api",
            "metadata": {"language": "ru", "file_type": "image/jpeg", "content_type": "handwritten"}
        }
    ]

    # Test Text Processor
    logger.info("\n📝 Testing Text Processor")
    text_processor = TextProcessor()

    for i, input_data in enumerate(test_inputs[:4], 1):
        input_obj = InputData(**input_data)
        try:
            result = text_processor.process(input_obj)
            logger.info(f"   Input {i}: {input_data['content'][:30]}...")
            logger.info(f"   Selected provider: {result['metadata'].get('provider', 'unknown')}")
            logger.info(f"   Language: {input_data['metadata'].get('language', 'unknown')}")
            logger.info(f"   Content type: {input_data['metadata'].get('content_type', 'unknown')}")
            logger.info("   ---")
        except Exception as e:
            logger.error(f"   Input {i} failed: {e}")

    # Test Audio Transcriber
    logger.info("\n🎤 Testing Audio Transcriber")
    audio_transcriber = AudioTranscriber()

    input_data = InputData(**test_inputs[4])
    try:
        result = audio_transcriber.process(input_data)
        logger.info(f"   Selected provider: {result['metadata'].get('provider', 'unknown')}")
        logger.info(f"   Language: {test_inputs[4]['metadata'].get('language', 'unknown')}")
    except Exception as e:
        logger.error(f"   Audio test failed: {e}")

    # Test Image Processor
    logger.info("\n📷 Testing Image Processor")
    image_processor = ImageProcessor()

    input_data = InputData(**test_inputs[5])
    try:
        result = image_processor.process(input_data)
        logger.info(f"   Selected provider: {result['metadata'].get('provider', 'unknown')}")
        logger.info(f"   Language: {test_inputs[5]['metadata'].get('language', 'unknown')}")
        logger.info(f"   Content type: {test_inputs[5]['metadata'].get('content_type', 'unknown')}")
    except Exception as e:
        logger.error(f"   Image test failed: {e}")

    logger.info("\n✅ Provider selection test complete!")

if __name__ == "__main__":
    main()




