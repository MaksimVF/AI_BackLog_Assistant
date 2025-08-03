


"""
Simple test for document processor
"""

import tempfile
import os
from tools.document_processor import extract_document_content, detect_document_type

def test_document_processor():
    """Test the document processor with different file types."""

    # Create test files
    test_files = {
        'test.txt': "This is a test text file.\nIt contains multiple lines.",
        'test.csv': "name,age,city\nJohn,25,New York\nJane,30,London",
    }

    # Test text file processing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_files['test.txt'])
        txt_file_path = f.name

    try:
        print("Testing text file processing...")
        content = extract_document_content(txt_file_path)
        print(f"Text file content: {content}")

        file_type = detect_document_type(txt_file_path)
        print(f"Text file type: {file_type}")
    finally:
        os.unlink(txt_file_path)

    # Test CSV file processing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_files['test.csv'])
        csv_file_path = f.name

    try:
        print("Testing CSV file processing...")
        content = extract_document_content(csv_file_path)
        print(f"CSV file content: {content}")

        file_type = detect_document_type(csv_file_path)
        print(f"CSV file type: {file_type}")
    finally:
        os.unlink(csv_file_path)

if __name__ == "__main__":
    test_document_processor()


