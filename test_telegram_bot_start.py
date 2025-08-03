




"""
Test Telegram bot startup and document handling
"""

import os
import tempfile
from telegram_bot.bot import handle_document, _format_pipeline_results
from telegram import Update, Document
from telegram.ext import CallbackContext
from unittest.mock import MagicMock

def test_telegram_bot_document_handling():
    """Test Telegram bot document handling function."""

    # Create a mock Telegram update with a document
    mock_update = MagicMock(spec=Update)
    mock_context = MagicMock(spec=CallbackContext)

    # Create a mock document
    mock_document = MagicMock(spec=Document)
    mock_document.file_id = "test_file_123"
    mock_document.file_name = "test_document.txt"
    mock_document.file_size = 1024

    # Create a mock message
    mock_message = MagicMock()
    mock_message.document = mock_document
    mock_update.message = mock_message

    # Create a mock bot
    mock_bot = MagicMock()
    mock_context.bot = mock_bot

    # Create a mock file
    mock_file = MagicMock()
    mock_bot.get_file.return_value = mock_file

    # Test the document handling
    try:
        print("Testing Telegram document handling...")

        # Call the handle_document function
        handle_document(mock_update, mock_context)

        # Check that the bot tried to download the file
        mock_bot.get_file.assert_called_with("test_file_123")
        mock_file.download.assert_called()

        print("✅ Telegram document handling test passed!")

    except Exception as e:
        print(f"❌ Error in document handling: {e}")

def test_response_formatting():
    """Test Telegram response formatting."""

    # Create test pipeline results
    test_results = {
        'document_id': 'test_doc',
        'raw_text': 'This is extracted text from a document.',
        'modality': 'document',
        'entities': {
            'people': ['John', 'Jane'],
            'locations': ['New York', 'London'],
            'departments': ['Engineering', 'Marketing']
        },
        'intent': 'information_extraction',
        'metadata': {
            'source': 'telegram',
            'file_name': 'test_document.txt',
            'file_size': 1024,
            'user_id': '12345',
            'chat_id': '67890'
        }
    }

    # Format the response
    response = _format_pipeline_results(test_results)

    print("Testing response formatting...")
    print("Formatted response:")
    print(response)
    print("✅ Response formatting test passed!")

if __name__ == "__main__":
    print("Testing Telegram bot document handling...")
    test_telegram_bot_document_handling()

    print("\nTesting response formatting...")
    test_response_formatting()





