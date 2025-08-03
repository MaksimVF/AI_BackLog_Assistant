

# Telegram Document Integration with Pipeline System

## Overview

This document describes the integration of Telegram document handling with the AI Backlog Assistant pipeline system. The integration allows users to upload documents through Telegram, which are then processed by the pipeline system to extract meaningful information and provide recommendations.

## Changes Made

### 1. Document Processor Tool (`tools/document_processor.py`)

Created a new document processor that can handle various document types:
- PDF files (using PyMuPDF)
- DOCX files (using python-docx)
- TXT files (plain text)
- CSV files

The processor provides:
- `extract_document_content()`: Extracts text content from documents
- `detect_document_type()`: Detects file type based on MIME type and extension

### 2. Input Processing Pipeline Enhancements

Updated `pipelines/input_processing_pipeline.py` to:

- **Added document modality support**: Enhanced `_detect_modality()` to recognize document files
- **Added document processing**: Created `_process_document()` method that uses the document processor
- **Updated validation**: Modified `IPPOutputSchema` to include 'document' as a valid modality
- **Added import**: Added `from tools.document_processor import extract_document_content`

### 3. Telegram Bot Integration

Updated `telegram_bot/bot.py` to:

- **Enhanced document handling**: Modified `handle_document()` to integrate with the pipeline system
- **Added pipeline processing**: Used `MainPipelineCoordinator` to process documents end-to-end
- **Added response formatting**: Created `_format_pipeline_results()` to format pipeline output for Telegram
- **Added metadata**: Included Telegram-specific metadata (user_id, chat_id, source)

### 4. Dependency Updates

Added `python-docx` to `requirements.txt` for DOCX file support.

## How It Works

1. **Document Upload**: User uploads a document via Telegram
2. **File Download**: Telegram bot downloads the file to the `downloads/` directory
3. **Pipeline Processing**: The document is processed through the main pipeline coordinator:
   - Input Processing Pipeline extracts text and detects entities
   - Information Manipulation Pipeline analyzes the content
   - Output Pipeline generates recommendations
4. **Response Formatting**: Results are formatted for Telegram display
5. **User Notification**: Formatted results are sent back to the user

## Testing

Created test files to verify the integration:
- `test_document_processor.py`: Tests document extraction functionality
- `test_telegram_simple.py`: Tests Telegram response formatting
- `test_telegram_integration.py`: Tests pipeline integration (requires full dependencies)

## Example Workflow

1. User sends `/upload` command to Telegram bot
2. User uploads a PDF document
3. Bot responds with:
   ```
   Document received:
   📄 Name: document.pdf
   📏 Size: 12345 bytes
   ⏳ Processing...
   ```
4. After processing, bot sends analysis results:
   ```
   ✅ Analysis complete!

   📋 **Document Analysis**
   🔍 Modality: document
   🎯 Intent: information_extraction
   📄 File: document.pdf

   🏷️ **Key Entities**
   people: John, Jane
   locations: New York, London
   departments: Engineering, Marketing

   💡 **Recommendations**
   1. Review extracted entities for accuracy
   2. Consider additional analysis for specific domains
   3. Check for any missing information
   ```

## Future Enhancements

- Add support for more document types (e.g., Excel, PowerPoint)
- Enhance entity extraction for domain-specific content
- Add document-specific recommendations
- Implement error handling for large files
- Add progress updates during processing

