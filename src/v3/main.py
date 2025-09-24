





"""
Level 3 Main Module

Provides entry point for Level 3 processing with:
- Pipeline initialization
- Configuration
- Execution
"""

import logging
from typing import Dict, Any
from src.v3.pipelines.level3_pipeline import Level3Pipeline

logger = logging.getLogger(__name__)

def main():
    """Main entry point for Level 3 processing"""
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Level 3 processing")

    # Initialize pipeline
    pipeline = Level3Pipeline(max_workers=8)

    # Example data from Level 2
    example_data = {
        "document_id": "level3_example",
        "content": "This is an example document for Level 3 processing",
        "metadata": {
            "source": "api",
            "modality": "text"
        },
        "classification": {
            "category": "important",
            "domain": "system",
            "confidence": 0.8
        },
        "prioritization": {
            "priority_level": "high",
            "priority_score": 0.85
        },
        "reflection": {
            "quality_score": 0.75,
            "issues": ["Basic analysis completed"],
            "improvement_areas": ["Enhance with NLP models"]
        }
    }

    # Process through Level 3
    result = pipeline.process(example_data)

    # Log result
    logger.info(f"Level 3 processing result: {result}")

    # Return result
    return result

if __name__ == "__main__":
    main()





