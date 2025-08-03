



import os
import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from typing import Optional, Dict, Any, List

class GoogleDriveConnector:
    """Agent for interacting with Google Drive API"""

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.service = build('drive', 'v3', credentials=credentials)

    def upload_file(self, file_path: str, file_name: str = None, folder_id: str = None) -> Optional[Dict]:
        """Upload a file to Google Drive"""
        file_name = file_name or os.path.basename(file_path)
        file_metadata = {'name': file_name}

        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()

        return file

    def download_file(self, file_id: str, download_path: str) -> bool:
        """Download a file from Google Drive"""
        request = self.service.files().get_media(fileId=file_id)
        with open(download_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
        return True

    def list_files(self, query: str = None, folder_id: str = None) -> List[Dict]:
        """List files in Google Drive"""
        q = []
        if query:
            q.append(f"name contains '{query}'")
        if folder_id:
            q.append(f"'{folder_id}' in parents")

        query_str = ' and '.join(q) if q else None

        results = self.service.files().list(
            q=query_str,
            fields="files(id, name, mimeType, createdTime, modifiedTime, webViewLink)"
        ).execute()

        return results.get('files', [])

    def create_folder(self, folder_name: str, parent_id: str = None) -> Optional[Dict]:
        """Create a folder in Google Drive"""
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_id:
            file_metadata['parents'] = [parent_id]

        folder = self.service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()

        return folder

    def get_file_metadata(self, file_id: str) -> Optional[Dict]:
        """Get metadata for a file"""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id, name, mimeType, createdTime, modifiedTime, size, webViewLink'
            ).execute()
            return file
        except Exception as e:
            print(f"Error getting file metadata: {e}")
            return None

    def delete_file(self, file_id: str) -> bool:
        """Delete a file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def share_file(self, file_id: str, email: str, role: str = 'reader') -> Optional[Dict]:
        """Share a file with a user"""
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            result = self.service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id'
            ).execute()
            return result
        except Exception as e:
            print(f"Error sharing file: {e}")
            return None

# Example usage
if __name__ == '__main__':
    # This would come from your OAuth2 flow
    from google_auth import get_google_credentials
    credentials = get_google_credentials()

    if credentials:
        drive = GoogleDriveConnector(credentials)

        # Example: List files
        files = drive.list_files()
        print("Files in Google Drive:")
        for file in files:
            print(f"{file['name']} ({file['id']})")

        # Example: Upload a file
        if files:
            test_file = 'test_upload.txt'
            with open(test_file, 'w') as f:
                f.write('This is a test file for Google Drive upload')

            uploaded = drive.upload_file(test_file)
            print(f"Uploaded file: {uploaded}")

            # Clean up
            os.remove(test_file)
            drive.delete_file(uploaded['id'])
    else:
        print("No Google credentials found. Please authenticate first.")



