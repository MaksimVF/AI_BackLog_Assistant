





import unittest
import datetime
from unittest.mock import MagicMock, patch
from google_sheets_connector import GoogleSheetsConnector
from google_calendar_connector import GoogleCalendarConnector
from google_integration_examples import GoogleIntegrationAgent

class TestGoogleIntegration(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        # Mock credentials
        self.mock_credentials = MagicMock()

        # Create mock connectors
        self.mock_sheets = MagicMock(spec=GoogleSheetsConnector)
        self.mock_calendar = MagicMock(spec=GoogleCalendarConnector)

        # Create the integration agent with mock connectors
        self.integration_agent = GoogleIntegrationAgent(self.mock_credentials)
        self.integration_agent.sheets = self.mock_sheets
        self.integration_agent.calendar = self.mock_calendar

    def test_export_issues_to_sheet(self):
        """Test exporting issues to Google Sheets"""
        # Mock data
        issues = [
            {
                'id': 1,
                'title': 'Test Issue 1',
                'status': 'Open',
                'priority': 'High',
                'assignee': {'login': 'user1'},
                'created_at': '2023-01-01',
                'updated_at': '2023-01-02'
            }
        ]

        # Mock responses
        self.mock_sheets.create_spreadsheet.return_value = {
            'spreadsheetId': 'test_spreadsheet_id',
            'spreadsheetUrl': 'https://docs.google.com/test'
        }
        self.mock_sheets.write_data.return_value = True

        # Call the method
        result = self.integration_agent.export_issues_to_sheet(issues, 'Test Sheet')

        # Assertions
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['spreadsheet_id'], 'test_spreadsheet_id')
        self.assertEqual(result['rows_written'], 1)

        # Verify that the methods were called
        self.mock_sheets.create_spreadsheet.assert_called_once()
        self.mock_sheets.write_data.assert_called_once()

    def test_schedule_issue_review(self):
        """Test scheduling an issue review"""
        # Mock data
        issue = {
            'id': 1,
            'title': 'Test Issue',
            'body': 'Test description'
        }

        # Mock responses
        self.mock_calendar.create_event.return_value = {
            'id': 'test_event_id',
            'htmlLink': 'https://calendar.google.com/test',
            'start': {'dateTime': '2023-01-01T12:00:00Z'},
            'end': {'dateTime': '2023-01-01T12:30:00Z'}
        }

        # Call the method
        result = self.integration_agent.schedule_issue_review(
            issue,
            'primary',
            ['test@example.com']
        )

        # Assertions
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['event_id'], 'test_event_id')
        self.assertEqual(result['event_url'], 'https://calendar.google.com/test')

        # Verify that the method was called
        self.mock_calendar.create_event.assert_called_once()

    def test_generate_project_timeline(self):
        """Test generating a project timeline"""
        # Mock data
        issues = [
            {
                'id': 1,
                'title': 'Test Issue 1',
                'body': 'Test description 1',
                'due_date': '2023-01-20T17:00:00Z'
            },
            {
                'id': 2,
                'title': 'Test Issue 2',
                'body': 'Test description 2',
                'due_date': '2023-01-25T17:00:00Z'
            }
        ]

        # Mock responses
        self.mock_calendar.create_event.side_effect = [
            {'id': 'event1', 'htmlLink': 'https://calendar.google.com/event1'},
            {'id': 'event2', 'htmlLink': 'https://calendar.google.com/event2'}
        ]

        # Call the method
        result = self.integration_agent.generate_project_timeline(issues, 'primary')

        # Assertions
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['events_created'], 2)
        self.assertEqual(len(result['events']), 2)

        # Verify that the method was called twice
        self.assertEqual(self.mock_calendar.create_event.call_count, 2)

    def test_sync_issue_status(self):
        """Test syncing issue status"""
        # Mock data
        issue = {
            'id': 1,
            'title': 'Test Issue',
            'status': 'Completed',
            'priority': 'High',
            'assignee': {'login': 'user1'},
            'created_at': '2023-01-01',
            'updated_at': '2023-01-02'
        }

        # Mock responses
        self.mock_sheets.read_data.return_value = [
            ['ID', 'Title', 'Status', 'Priority', 'Assignee', 'Created At', 'Updated At'],
            ['1', 'Test Issue', 'Open', 'High', 'user1', '2023-01-01', '2023-01-02']
        ]
        self.mock_sheets.write_data.return_value = True

        # Call the method
        result = self.integration_agent.sync_issue_status(
            issue,
            'test_spreadsheet_id',
            'Issues'
        )

        # Assertions
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['row_updated'], 2)

        # Verify that the methods were called
        self.mock_sheets.read_data.assert_called_once()
        self.mock_sheets.write_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()





