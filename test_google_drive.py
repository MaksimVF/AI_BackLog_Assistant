




import unittest
import os
import json
from unittest.mock import patch, MagicMock
from google_drive_connector import GoogleDriveConnector
from google_drive_integration import GoogleDriveAgent

class TestGoogleDriveIntegration(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        # Mock credentials
        self.mock_credentials = MagicMock()
        self.drive_connector = GoogleDriveConnector(self.mock_credentials)
        self.drive_agent = GoogleDriveAgent(self.mock_credentials)

        # Mock the service
        self.drive_connector.service = MagicMock()

    def test_backup_issue_data(self):
        """Test backing up issue data"""
        # Mock the necessary methods
        self.drive_connector.list_files.return_value = []
        self.drive_connector.create_folder.return_value = {'id': 'folder_id'}
        self.drive_connector.upload_file.return_value = {
            'id': 'file_id',
            'name': 'issue_123.json',
            'webViewLink': 'https://drive.google.com/file_id'
        }

        # Test data
        issue_data = {
            'id': 123,
            'title': 'Test Issue',
            'description': 'Test description'
        }

        # Call the method
        result = self.drive_agent.backup_issue_data(issue_data)

        # Assertions
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['file_name'], 'issue_123.json')
        self.assertTrue('file_id' in result)

    def test_generate_report(self):
        """Test generating a report"""
        # Mock the necessary methods
        self.drive_connector.list_files.return_value = []
        self.drive_connector.create_folder.return_value = {'id': 'folder_id'}
        self.drive_connector.upload_file.return_value = {
            'id': 'file_id',
            'name': 'Test Report.md',
            'webViewLink': 'https://drive.google.com/file_id'
        }

        # Test data
        report_data = {
            'Summary': 'Test summary',
            'Details': 'Test details'
        }

        # Call the method
        result = self.drive_agent.generate_report(report_data, 'Test Report')

        # Assertions
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['file_name'], 'Test Report.md')
        self.assertTrue('file_id' in result)

    def test_share_document(self):
        """Test sharing a document"""
        # Mock the share_file method
        self.drive_connector.share_file.return_value = {'id': 'permission_id'}

        # Test data
        emails = ['test1@example.com', 'test2@example.com']

        # Call the method
        result = self.drive_agent.share_document('file_id', emails)

        # Assertions
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['shared_with'], 2)
        self.assertEqual(len(result['results']), 2)
        self.assertEqual(result['results'][0]['status'], 'success')

    def test_get_document_content(self):
        """Test getting document content"""
        # Mock the necessary methods
        self.drive_connector.get_file_metadata.return_value = {
            'id': 'file_id',
            'name': 'test.json',
            'mimeType': 'application/json'
        }
        self.drive_connector.download_file.return_value = True

        # Create a test file
        test_file = '/tmp/file_id_test.json'
        with open(test_file, 'w') as f:
            json.dump({'test': 'data'}, f)

        # Patch the open function to return our test file content
        with patch('builtins.open', return_value=open(test_file, 'r')):
            result = self.drive_agent.get_document_content('file_id')

            # Assertions
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['file_name'], 'test.json')
            self.assertTrue('content' in result)

        # Clean up
        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()




