





import datetime
from typing import Dict, Any, List
from google_auth import get_google_credentials
from google_sheets_connector import GoogleSheetsConnector
from google_calendar_connector import GoogleCalendarConnector

class GoogleIntegrationAgent:
    """Agent for integrating Google services with the AI Backlog Assistant"""

    def __init__(self, credentials):
        self.sheets = GoogleSheetsConnector(credentials)
        self.calendar = GoogleCalendarConnector(credentials)

    def export_issues_to_sheet(self, issues: List[Dict], spreadsheet_name: str = 'Issue Tracker') -> Dict:
        """Export issues to a Google Sheet"""
        # Create a new spreadsheet
        spreadsheet = self.sheets.create_spreadsheet(spreadsheet_name)

        if not spreadsheet:
            return {'status': 'error', 'message': 'Failed to create spreadsheet'}

        # Prepare data for the sheet
        headers = ['ID', 'Title', 'Status', 'Priority', 'Assignee', 'Created At', 'Updated At']
        data = [headers]

        for issue in issues:
            row = [
                issue.get('id', ''),
                issue.get('title', ''),
                issue.get('status', ''),
                issue.get('priority', ''),
                issue.get('assignee', {}).get('login', '') if issue.get('assignee') else '',
                issue.get('created_at', ''),
                issue.get('updated_at', '')
            ]
            data.append(row)

        # Write data to the sheet
        success = self.sheets.write_data(spreadsheet['spreadsheetId'], 'Issues', data)

        if success:
            return {
                'status': 'success',
                'spreadsheet_id': spreadsheet['spreadsheetId'],
                'spreadsheet_url': spreadsheet['spreadsheetUrl'],
                'rows_written': len(data) - 1  # Exclude headers
            }
        else:
            return {'status': 'error', 'message': 'Failed to write data to spreadsheet'}

    def schedule_issue_review(self, issue: Dict, calendar_id: str, attendees: List[str]) -> Dict:
        """Schedule an issue review meeting"""
        # Set the meeting time (e.g., 1 hour from now)
        start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        end_time = start_time + datetime.timedelta(minutes=30)

        # Create the event
        event = self.calendar.create_event(
            calendar_id,
            f"Issue Review: {issue.get('title', 'Untitled')}",
            f"Review and discuss issue #{issue.get('id', 'unknown')}\n\n{issue.get('body', 'No description')}",
            start_time,
            end_time,
            attendees
        )

        if event:
            return {
                'status': 'success',
                'event_id': event['id'],
                'event_url': event['htmlLink'],
                'start_time': event['start']['dateTime'],
                'end_time': event['end']['dateTime']
            }
        else:
            return {'status': 'error', 'message': 'Failed to create calendar event'}

    def generate_project_timeline(self, issues: List[Dict], calendar_id: str) -> Dict:
        """Generate a project timeline in Google Calendar"""
        created_events = []

        for issue in issues:
            # Skip issues without due dates
            if not issue.get('due_date'):
                continue

            # Parse the due date
            try:
                due_date = datetime.datetime.fromisoformat(issue.get('due_date').replace('Z', '+00:00'))
            except (ValueError, TypeError):
                continue

            # Create a calendar event for the issue
            event = self.calendar.create_event(
                calendar_id,
                f"Deadline: {issue.get('title', 'Untitled')}",
                f"Issue #{issue.get('id', 'unknown')} is due\n\n{issue.get('body', 'No description')}",
                due_date - datetime.timedelta(hours=1),  # Reminder 1 hour before
                due_date,
                []  # No attendees for timeline events
            )

            if event:
                created_events.append({
                    'issue_id': issue.get('id'),
                    'event_id': event['id'],
                    'event_url': event['htmlLink']
                })

        return {
            'status': 'success',
            'events_created': len(created_events),
            'events': created_events
        }

    def sync_issue_status(self, issue: Dict, spreadsheet_id: str, sheet_name: str) -> Dict:
        """Sync issue status to a Google Sheet"""
        # Find the issue row in the sheet
        data = self.sheets.read_data(spreadsheet_id, sheet_name)

        if not data or len(data) < 2:  # No headers or data
            return {'status': 'error', 'message': 'No data found in sheet'}

        # Find the issue row (skip header)
        issue_row = None
        for i, row in enumerate(data[1:], start=2):  # Start from row 2
            if str(row[0]) == str(issue.get('id')):
                issue_row = i
                break

        if not issue_row:
            return {'status': 'error', 'message': 'Issue not found in sheet'}

        # Update the issue data
        data[issue_row - 1] = [
            issue.get('id', ''),
            issue.get('title', ''),
            issue.get('status', ''),
            issue.get('priority', ''),
            issue.get('assignee', {}).get('login', '') if issue.get('assignee') else '',
            issue.get('created_at', ''),
            issue.get('updated_at', '')
        ]

        # Write the updated data back to the sheet
        success = self.sheets.write_data(spreadsheet_id, sheet_name, data)

        if success:
            return {'status': 'success', 'row_updated': issue_row}
        else:
            return {'status': 'error', 'message': 'Failed to update sheet'}

# Example usage
if __name__ == '__main__':
    # Get Google credentials
    credentials = get_google_credentials()

    if credentials:
        google_agent = GoogleIntegrationAgent(credentials)

        # Example issue data
        issues = [
            {
                'id': 1,
                'title': 'Implement Google Sheets Integration',
                'status': 'In Progress',
                'priority': 'High',
                'assignee': {'login': 'developer1'},
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-10T12:00:00Z',
                'body': 'Implement Google Sheets integration for data export',
                'due_date': '2023-01-20T17:00:00Z'
            },
            {
                'id': 2,
                'title': 'Add Calendar Integration',
                'status': 'Open',
                'priority': 'Medium',
                'assignee': {'login': 'developer2'},
                'created_at': '2023-01-02T00:00:00Z',
                'updated_at': '2023-01-05T10:00:00Z',
                'body': 'Add Google Calendar integration for scheduling',
                'due_date': '2023-01-25T17:00:00Z'
            }
        ]

        # Example: Export issues to Google Sheets
        export_result = google_agent.export_issues_to_sheet(issues)
        print("Export result:", export_result)

        if export_result['status'] == 'success':
            # Example: Schedule an issue review
            review_result = google_agent.schedule_issue_review(
                issues[0],
                'primary',
                ['team@example.com', 'manager@example.com']
            )
            print("Review scheduling result:", review_result)

            # Example: Generate project timeline
            timeline_result = google_agent.generate_project_timeline(issues, 'primary')
            print("Timeline generation result:", timeline_result)

            # Example: Sync issue status
            status_update = issues[0].copy()
            status_update['status'] = 'Completed'
            sync_result = google_agent.sync_issue_status(
                status_update,
                export_result['spreadsheet_id'],
                'Issues'
            )
            print("Status sync result:", sync_result)
    else:
        print("Please authenticate with Google first")





