





"""
Main entry point for AI Backlog Assistant v2.0
"""

import logging
import sys
from src.common.utils import setup_logging
from src.v2.pipelines.level1_pipeline import Level1Pipeline

def main():
    """Main function to demonstrate Level 1 processing"""
    # Set up logging
    setup_logging(log_level="INFO")

    logger = logging.getLogger("ai_backlog_assistant")
    logger.info("🚀 Starting AI Backlog Assistant v2.0")

    # Create Level 1 pipeline
    pipeline = Level1Pipeline()

    # Example inputs to test
    test_inputs = [
        {
            "content": "I have an idea for a new feature: dark mode support",
            "source": "api",
            "metadata": {"user": "user123"}
        },
        {
            "content": "The app crashes when I try to login with Google",
            "source": "telegram",
            "metadata": {"user": "telegram_user456"}
        },
        {
            "content": "I love the new update! Much faster now.",
            "source": "web",
            "metadata": {"user": "web_user789"}
        },
        {
            "content": "This is simulated audio content that would be transcribed",
            "source": "api",
            "metadata": {"file_type": "audio/mp3", "user": "user_audio"}
        }
    ]

    # Process each input
    for i, input_data in enumerate(test_inputs, 1):
        logger.info(f"\n📦 Processing input {i}/{len(test_inputs)}")
        logger.info(f"Input: {input_data['content'][:50]}...")

        try:
            result = pipeline.process(input_data)

            # Display results
            logger.info("✅ Processing successful!")
            logger.info(f"   Modality: {result['modality']}")
            logger.info(f"   Content Type: {result['processed_data']['metadata'].get('content_type', 'unknown')}")
            logger.info(f"   Emotion: {result['processed_data']['metadata'].get('emotion', 'unknown')}")
            logger.info(f"   Initial Score: {result['processed_data']['metadata'].get('initial_score', 0):.2f}")
            logger.info(f"   Trigger Level 2: {result['trigger_level2']}")

        except Exception as e:
            logger.error(f"❌ Processing failed: {e}")

    logger.info("\n🎉 Level 1 pipeline demonstration complete!")

if __name__ == "__main__":
    main()





