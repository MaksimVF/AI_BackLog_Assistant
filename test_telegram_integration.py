



"""
Test Telegram integration with pipeline system
"""

import tempfile
import os
from tools.document_processor import extract_document_content
from pipelines.input_processing_pipeline import InputProcessingPipeline

def test_telegram_pipeline_integration():
    """Test the Telegram pipeline integration."""

    # Create test files
    test_files = {
        'test.txt': "This is a test text file.\nIt contains multiple lines of content.\nThe pipeline should process this text and extract entities and intent.",
        'test.csv': "name,age,city,department\nJohn,25,New York,Engineering\nJane,30,London,Marketing",
    }

    # Test text file processing through the pipeline
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_files['test.txt'])
        txt_file_path = f.name

    try:
        print("Testing text file processing through pipeline...")

        # Create pipeline
        pipeline = InputProcessingPipeline()

        # Process through pipeline
        result = pipeline.process({
            'document_id': 'telegram_test_txt',
            'raw_content': txt_file_path,
            'metadata': {
                'source': 'telegram',
                'file_name': 'test.txt',
                'user_id': '12345',
                'chat_id': '67890'
            }
        })

        print(f"Pipeline result: {result}")

    finally:
        os.unlink(txt_file_path)

    # Test CSV file processing through the pipeline
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_files['test.csv'])
        csv_file_path = f.name

    try:
        print("Testing CSV file processing through pipeline...")

        # Process through pipeline
        result = pipeline.process({
            'document_id': 'telegram_test_csv',
            'raw_content': csv_file_path,
            'metadata': {
                'source': 'telegram',
                'file_name': 'test.csv',
                'user_id': '12345',
                'chat_id': '67890'
            }
        })

        print(f"Pipeline result: {result}")

    finally:
        os.unlink(csv_file_path)

if __name__ == "__main__":
    test_telegram_pipeline_integration()



