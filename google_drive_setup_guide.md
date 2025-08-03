



# Google Drive Integration Setup Guide

## 1. Create Google API Credentials

1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select an existing project
3. Go to APIs & Services > Credentials
4. Click "Create Credentials" > "OAuth 2.0 Client IDs"
5. Configure the consent screen if you haven't already
6. Set Application type to "Web application"
7. Add the following authorized redirect URIs:
   - http://localhost:5006/google/callback
8. Click "Create"
9. Download the JSON file and save it as `client_secret.json` in your project directory

## 2. Enable Google Drive API

1. In the Google Cloud Console, go to APIs & Services > Library
2. Search for "Google Drive API" and click on it
3. Click "Enable"

## 3. Install Required Libraries

Make sure you have the Google client libraries installed:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## 4. Running the Services

1. Start the Google OAuth server:
   ```bash
   python google_auth.py
   ```

2. Open http://localhost:5006/google/login to authenticate with Google

3. After authentication, you can use the GoogleDriveConnector to interact with Google Drive

## 5. Integrating with Your Main Application

You can now integrate the GoogleDriveConnector with your existing agent system. Here's an example of how to use it:

```python
from google_auth import get_google_credentials
from google_drive_connector import GoogleDriveConnector

# Get credentials from the OAuth flow
credentials = get_google_credentials()

if credentials:
    drive = GoogleDriveConnector(credentials)

    # List files
    files = drive.list_files()
    print("Files:", files)

    # Upload a file
    uploaded = drive.upload_file("path/to/your/file.txt")
    print("Uploaded:", uploaded)

    # Download a file
    downloaded = drive.download_file(uploaded['id'], "path/to/save/file.txt")
    print("Downloaded:", downloaded)
```

## 6. Integration Scenarios

Here are some ways you can integrate Google Drive with your AI Backlog Assistant:

1. **Document Storage**: Store generated reports, summaries, and other documents
2. **File Sharing**: Share documents with team members
3. **Backup**: Backup important data to Google Drive
4. **Collaboration**: Enable collaborative editing of documents
5. **AI Analysis**: Upload documents for AI analysis and processing



