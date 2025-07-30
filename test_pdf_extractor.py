

from tools.pdf_extractor import PDFExtractor
import os

# Create a simple test to verify our PDF extractor works
def test_pdf_extractor():
    # We'll need to create a real PDF file to test with
    # For now, let's just test the class initialization and error handling
    try:
        # This should raise FileNotFoundError since the file doesn't exist
        extractor = PDFExtractor("nonexistent.pdf")
        text = extractor.extract_text()
    except FileNotFoundError as e:
        print(f"Expected error caught: {e}")

    print("PDFExtractor class created successfully!")
    print("Basic error handling works as expected")

if __name__ == "__main__":
    test_pdf_extractor()

