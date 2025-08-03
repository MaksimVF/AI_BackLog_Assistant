




import os
import json
from typing import Dict, Any, List
from google_auth import get_google_credentials
from google_drive_connector import GoogleDriveConnector

class GoogleDriveAgent:
    """Agent for integrating Google Drive with the AI Backlog Assistant"""

    def __init__(self, credentials):
        self.drive = GoogleDriveConnector(credentials)

    def backup_issue_data(self, issue_data: Dict, folder_name: str = 'Issue Backups') -> Dict:
        """Backup issue data to Google Drive"""
        # Create or find backup folder
        folders = self.drive.list_files(query=folder_name, folder_id=None)
        folder = folders[0] if folders else None

        if not folder:
            folder = self.drive.create_folder(folder_name)

        # Create a JSON file with issue data
        issue_id = issue_data.get('id', 'unknown')
        file_name = f"issue_{issue_id}.json"
        file_path = f"/tmp/{file_name}"

        with open(file_path, 'w') as f:
            json.dump(issue_data, f, indent=2)

        # Upload to Google Drive
        uploaded = self.drive.upload_file(file_path, file_name, folder['id'])

        # Clean up local file
        os.remove(file_path)

        return {
            'status': 'success',
            'file_id': uploaded['id'],
            'file_name': uploaded['name'],
            'web_link': uploaded['webViewLink']
        }

    def generate_report(self, report_data: Dict, report_name: str, folder_name: str = 'Reports') -> Dict:
        """Generate and upload a report to Google Drive"""
        # Create or find reports folder
        folders = self.drive.list_files(query=folder_name, folder_id=None)
        folder = folders[0] if folders else None

        if not folder:
            folder = self.drive.create_folder(folder_name)

        # Create a report file
        file_name = f"{report_name}.md"
        file_path = f"/tmp/{file_name}"

        with open(file_path, 'w') as f:
            f.write(f"# {report_name}\n\n")
            for section, content in report_data.items():
                f.write(f"## {section}\n\n{content}\n\n")

        # Upload to Google Drive
        uploaded = self.drive.upload_file(file_path, file_name, folder['id'])

        # Clean up local file
        os.remove(file_path)

        return {
            'status': 'success',
            'file_id': uploaded['id'],
            'file_name': uploaded['name'],
            'web_link': uploaded['webViewLink']
        }

    def share_document(self, file_id: str, emails: List[str], role: str = 'reader') -> Dict:
        """Share a document with team members"""
        results = []
        for email in emails:
            result = self.drive.share_file(file_id, email, role)
            if result:
                results.append({
                    'email': email,
                    'status': 'success',
                    'permission_id': result['id']
                })
            else:
                results.append({
                    'email': email,
                    'status': 'failed'
                })

        return {
            'status': 'completed',
            'shared_with': len(results),
            'results': results
        }

    def get_document_content(self, file_id: str) -> Dict:
        """Get the content of a document from Google Drive"""
        file_metadata = self.drive.get_file_metadata(file_id)

        if not file_metadata:
            return {'status': 'error', 'message': 'File not found'}

        # Download the file
        temp_path = f"/tmp/{file_id}_{file_metadata['name']}"
        if self.drive.download_file(file_id, temp_path):
            # Read the content
            with open(temp_path, 'r') as f:
                content = f.read()

            # Clean up
            os.remove(temp_path)

            return {
                'status': 'success',
                'file_name': file_metadata['name'],
                'content': content,
                'mime_type': file_metadata['mimeType']
            }
        else:
            return {'status': 'error', 'message': 'Failed to download file'}

# Example usage
if __name__ == '__main__':
    # Get Google credentials
    credentials = get_google_credentials()

    if credentials:
        drive_agent = GoogleDriveAgent(credentials)

        # Example issue data
        issue_data = {
            'id': 123,
            'title': 'Test Issue',
            'description': 'This is a test issue for Google Drive integration',
            'status': 'open',
            'comments': 2,
            'created_at': '2023-01-01T00:00:00Z'
        }

        # Backup issue data
        backup_result = drive_agent.backup_issue_data(issue_data)
        print("Backup result:", backup_result)

        # Generate a report
        report_data = {
            'Summary': 'This is a summary of the report',
            'Details': 'Detailed information about the report',
            'Conclusion': 'Final conclusions and recommendations'
        }
        report_result = drive_agent.generate_report(report_data, 'Test Report')
        print("Report result:", report_result)

        # Share the report
        share_result = drive_agent.share_document(
            report_result['file_id'],
            ['test@example.com', 'user@example.com']
        )
        print("Share result:", share_result)

        # Get document content
        content_result = drive_agent.get_document_content(backup_result['file_id'])
        print("Content result:", content_result)
    else:
        print("Please authenticate with Google first")




