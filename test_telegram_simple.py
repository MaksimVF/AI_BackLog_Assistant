




"""
Simple test for Telegram document processing
"""

import tempfile
import os
from tools.document_processor import extract_document_content, detect_document_type

def test_telegram_document_processing():
    """Test Telegram document processing."""

    # Create test files
    test_files = {
        'test.txt': "This is a test text file.\nIt contains multiple lines of content.\nThe pipeline should process this text and extract entities and intent.",
        'test.csv': "name,age,city,department\nJohn,25,New York,Engineering\nJane,30,London,Marketing",
    }

    # Test text file processing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_files['test.txt'])
        txt_file_path = f.name

    try:
        print("Testing text file processing...")

        # Extract content
        content = extract_document_content(txt_file_path)
        print(f"Extracted content: {content}")

        # Simulate pipeline processing
        result = {
            'document_id': 'telegram_test_txt',
            'raw_text': content,
            'modality': 'document',
            'entities': {
                'people': ['John', 'Jane'],
                'locations': ['New York', 'London'],
                'departments': ['Engineering', 'Marketing']
            },
            'intent': 'information_extraction',
            'metadata': {
                'source': 'telegram',
                'file_name': 'test.txt',
                'file_type': detect_document_type(txt_file_path)
            }
        }

        # Format response for Telegram
        response = format_telegram_response(result)
        print(f"Telegram response: {response}")

    finally:
        os.unlink(txt_file_path)

def format_telegram_response(result: dict) -> str:
    """Format pipeline results for Telegram response."""
    try:
        # Extract key information from pipeline results
        modality = result.get('modality', 'unknown')
        intent = result.get('intent', 'unknown')
        entities = result.get('entities', {})
        metadata = result.get('metadata', {})

        # Build response text
        response = "✅ Analysis complete!\n\n"
        response += f"📋 **Document Analysis**\n"
        response += f"🔍 Modality: {modality}\n"
        response += f"🎯 Intent: {intent}\n"
        response += f"📄 File: {metadata.get('file_name', 'unknown')}\n"

        if entities:
            response += "\n🏷️ **Key Entities**\n"
            for entity_type, entity_values in entities.items():
                if isinstance(entity_values, list):
                    response += f"{entity_type}: {', '.join(entity_values[:3])}\n"
                else:
                    response += f"{entity_type}: {entity_values}\n"

        response += "\n💡 **Recommendations**\n"
        response += "1. Review extracted entities for accuracy\n"
        response += "2. Consider additional analysis for specific domains\n"
        response += "3. Check for any missing information"

        return response

    except Exception as e:
        return f"❌ Error formatting results: {str(e)}"

if __name__ == "__main__":
    test_telegram_document_processing()




