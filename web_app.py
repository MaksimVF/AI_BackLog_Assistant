



import os
from flask import Flask, render_template, redirect, url_for, session, request
from google_auth import get_google_credentials
from google_drive_connector import GoogleDriveConnector
from google_sheets_connector import GoogleSheetsConnector
from google_calendar_connector import GoogleCalendarConnector

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Mock data for demonstration
ISSUES = [
    {
        'id': 1,
        'title': 'Implement Google Sheets Integration',
        'status': 'In Progress',
        'priority': 'High',
        'assignee': 'developer1',
        'created_at': '2023-01-01',
        'updated_at': '2023-01-10'
    },
    {
        'id': 2,
        'title': 'Add Calendar Integration',
        'status': 'Open',
        'priority': 'Medium',
        'assignee': 'developer2',
        'created_at': '2023-01-02',
        'updated_at': '2023-01-05'
    }
]

@app.route('/')
def home():
    """Home page with issue list"""
    return render_template('home.html', issues=ISSUES)

@app.route('/settings')
def settings():
    """Settings page with integration configuration"""
    # Check Google authentication status
    google_connected = bool(session.get('google_credentials'))

    # Get Google services status
    drive_status = 'Connected' if google_connected else 'Disconnected'
    sheets_status = 'Connected' if google_connected else 'Disconnected'
    calendar_status = 'Connected' if google_connected else 'Disconnected'

    return render_template('settings.html',
                         google_connected=google_connected,
                         drive_status=drive_status,
                         sheets_status=sheets_status,
                         calendar_status=calendar_status)

@app.route('/google/login')
def google_login():
    """Redirect to Google OAuth2 login"""
    return redirect('http://localhost:5006/google/login')

@app.route('/google/callback')
def google_callback():
    """Handle Google OAuth2 callback"""
    # This would be handled by the google_auth.py server
    # For this example, we'll just redirect to settings
    return redirect(url_for('settings'))

@app.route('/issue/<int:issue_id>')
def issue_detail(issue_id):
    """Issue detail page"""
    issue = next((i for i in ISSUES if i['id'] == issue_id), None)
    if not issue:
        return "Issue not found", 404

    # Check if we have Google credentials for integration features
    google_connected = bool(session.get('google_credentials'))

    return render_template('issue_detail.html',
                         issue=issue,
                         google_connected=google_connected)

@app.route('/export_to_sheets')
def export_to_sheets():
    """Export issues to Google Sheets"""
    credentials = get_google_credentials()
    if not credentials:
        return redirect(url_for('google_login'))

    # Export issues to Google Sheets
    sheets = GoogleSheetsConnector(credentials)
    spreadsheet = sheets.create_spreadsheet('Issue Export')

    if spreadsheet:
        # Prepare data
        headers = ['ID', 'Title', 'Status', 'Priority', 'Assignee', 'Created At', 'Updated At']
        data = [headers]
        for issue in ISSUES:
            data.append([
                issue['id'],
                issue['title'],
                issue['status'],
                issue['priority'],
                issue['assignee'],
                issue['created_at'],
                issue['updated_at']
            ])

        # Write data
        sheets.write_data(spreadsheet['spreadsheetId'], 'Issues', data)

        return redirect(spreadsheet['spreadsheetUrl'])
    else:
        return "Failed to create spreadsheet", 500

@app.route('/schedule_review/<int:issue_id>')
def schedule_review(issue_id):
    """Schedule an issue review meeting"""
    credentials = get_google_credentials()
    if not credentials:
        return redirect(url_for('google_login'))

    # Find the issue
    issue = next((i for i in ISSUES if i['id'] == issue_id), None)
    if not issue:
        return "Issue not found", 404

    # Schedule a meeting
    calendar = GoogleCalendarConnector(credentials)
    start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(minutes=30)

    event = calendar.create_event(
        'primary',
        f"Issue Review: {issue['title']}",
        f"Review and discuss issue #{issue['id']}",
        start_time,
        end_time,
        ['team@example.com']
    )

    if event:
        return redirect(event['htmlLink'])
    else:
        return "Failed to create event", 500

if __name__ == '__main__':
    app.run(port=5007, debug=True)



