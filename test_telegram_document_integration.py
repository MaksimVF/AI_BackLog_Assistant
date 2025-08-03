

"""
Test Telegram Document Integration with Pipeline System
"""

import os
import tempfile
from pipelines.main_pipeline_coordinator import MainPipelineCoordinator
from tools.document_processor import extract_document_content, detect_document_type

def test_document_processing():
    """Test document processing with different file types."""

    # Create test files
    test_files = {
        'test.txt': "This is a test text file.\nIt contains multiple lines.",
        'test.csv': "name,age,city\nJohn,25,New York\nJane,30,London",
    }

    # Test PDF processing (if we have a sample PDF)
    pdf_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))

    coordinator = MainPipelineCoordinator()

    # Test text file processing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_files['test.txt'])
        txt_file_path = f.name

    try:
        print("Testing text file processing...")
        result = coordinator.process_end_to_end(
            document_id="test_txt",
            raw_content=txt_file_path,
            metadata={'source': 'test'}
        )
        print(f"Text file result: {result}")
    finally:
        os.unlink(txt_file_path)

    # Test CSV file processing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_files['test.csv'])
        csv_file_path = f.name

    try:
        print("Testing CSV file processing...")
        result = coordinator.process_end_to_end(
            document_id="test_csv",
            raw_content=csv_file_path,
            metadata={'source': 'test'}
        )
        print(f"CSV file result: {result}")
    finally:
        os.unlink(csv_file_path)

    # Test PDF processing if available
    if pdf_files:
        print("Testing PDF file processing...")
        result = coordinator.process_end_to_end(
            document_id="test_pdf",
            raw_content=pdf_files[0],
            metadata={'source': 'test'}
        )
        print(f"PDF file result: {result}")
    else:
        print("No PDF files found for testing")

def test_document_extractor():
    """Test the document extractor directly."""

    # Create test files
    test_files = {
        'test.txt': "This is a test text file.\nIt contains multiple lines.",
        'test.csv': "name,age,city\nJohn,25,New York\nJane,30,London",
    }

    # Test text extraction
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_files['test.txt'])
        txt_file_path = f.name

    try:
        content = extract_document_content(txt_file_path)
        print(f"Text file content: {content}")

        file_type = detect_document_type(txt_file_path)
        print(f"Text file type: {file_type}")
    finally:
        os.unlink(txt_file_path)

    # Test CSV extraction
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_files['test.csv'])
        csv_file_path = f.name

    try:
        content = extract_document_content(csv_file_path)
        print(f"CSV file content: {content}")

        file_type = detect_document_type(csv_file_path)
        print(f"CSV file type: {file_type}")
    finally:
        os.unlink(csv_file_path)

if __name__ == "__main__":
    print("Testing document extractor...")
    test_document_extractor()

    print("\nTesting pipeline integration...")
    test_document_processing()

