



import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Optional, Dict, Any, List

class GoogleSheetsConnector:
    """Agent for interacting with Google Sheets API"""

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.service = build('sheets', 'v4', credentials=credentials)

    def create_spreadsheet(self, title: str) -> Optional[Dict]:
        """Create a new Google Sheet"""
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        result = self.service.spreadsheets().create(
            body=spreadsheet,
            fields='spreadsheetId,spreadsheetUrl'
        ).execute()

        return result

    def get_spreadsheet(self, spreadsheet_id: str) -> Optional[Dict]:
        """Get spreadsheet metadata"""
        try:
            result = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                fields='properties,sheets'
            ).execute()
            return result
        except Exception as e:
            print(f"Error getting spreadsheet: {e}")
            return None

    def write_data(self, spreadsheet_id: str, sheet_name: str, data: List[List[Any]], start_cell: str = 'A1') -> bool:
        """Write data to a Google Sheet"""
        try:
            # Get sheet ID by name
            spreadsheet = self.get_spreadsheet(spreadsheet_id)
            sheet_id = None
            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == sheet_name:
                    sheet_id = sheet['properties']['sheetId']
                    break

            if not sheet_id:
                print(f"Sheet '{sheet_name}' not found")
                return False

            # Prepare the request
            range_name = f"{sheet_name}!{start_cell}"
            body = {
                'values': data
            }

            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            return True
        except Exception as e:
            print(f"Error writing data: {e}")
            return False

    def read_data(self, spreadsheet_id: str, sheet_name: str, range_name: str = 'A1:Z1000') -> Optional[List[List[Any]]]:
        """Read data from a Google Sheet"""
        try:
            range_full = f"{sheet_name}!{range_name}"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_full
            ).execute()

            return result.get('values', [])
        except Exception as e:
            print(f"Error reading data: {e}")
            return None

    def add_sheet(self, spreadsheet_id: str, title: str) -> Optional[Dict]:
        """Add a new sheet to a spreadsheet"""
        try:
            requests = [{
                'addSheet': {
                    'properties': {
                        'title': title
                    }
                }
            }]

            body = {
                'requests': requests
            }

            result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body
            ).execute()

            return result
        except Exception as e:
            print(f"Error adding sheet: {e}")
            return None

    def share_spreadsheet(self, spreadsheet_id: str, email: str, role: str = 'writer') -> Optional[Dict]:
        """Share a spreadsheet with a user"""
        try:
            # Use the drive service for sharing
            drive_service = build('drive', 'v3', credentials=self.credentials)
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            result = drive_service.permissions().create(
                fileId=spreadsheet_id,
                body=permission,
                fields='id'
            ).execute()
            return result
        except Exception as e:
            print(f"Error sharing spreadsheet: {e}")
            return None

# Example usage
if __name__ == '__main__':
    from google_auth import get_google_credentials

    # Get Google credentials
    credentials = get_google_credentials()

    if credentials:
        sheets = GoogleSheetsConnector(credentials)

        # Example: Create a spreadsheet
        spreadsheet = sheets.create_spreadsheet('Test Spreadsheet')
        print("Created spreadsheet:", spreadsheet)

        if spreadsheet:
            # Example: Write data
            data = [
                ['Issue ID', 'Title', 'Status', 'Priority'],
                [1, 'Test Issue 1', 'Open', 'High'],
                [2, 'Test Issue 2', 'In Progress', 'Medium'],
                [3, 'Test Issue 3', 'Closed', 'Low']
            ]
            success = sheets.write_data(spreadsheet['spreadsheetId'], 'Sheet1', data)
            print("Write data success:", success)

            # Example: Read data
            read_data = sheets.read_data(spreadsheet['spreadsheetId'], 'Sheet1')
            print("Read data:", read_data)

            # Example: Share spreadsheet
            share_result = sheets.share_spreadsheet(spreadsheet['spreadsheetId'], 'test@example.com')
            print("Share result:", share_result)
    else:
        print("Please authenticate with Google first")




