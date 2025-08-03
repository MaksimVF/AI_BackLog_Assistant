


import os
import json
from flask import Flask, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = 'your_client_id'
GOOGLE_CLIENT_SECRET = 'your_client_secret'
GOOGLE_REDIRECT_URI = 'http://localhost:5006/google/callback'

# Scopes required for Google Drive access
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/drive.metadata.readonly']

# Path to client secrets file
CLIENT_SECRETS_FILE = 'client_secret.json'

@app.route('/google/login')
def google_login():
    """Redirect user to Google for authorization"""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state
    return redirect(authorization_url)

@app.route('/google/callback')
def google_callback():
    """Handle Google OAuth2 callback"""
    state = session['state']

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=GOOGLE_SCOPES,
        state=state,
        redirect_uri=GOOGLE_REDIRECT_URI)

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['google_credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect(url_for('google_success'))

@app.route('/google/success')
def google_success():
    """Show successful authentication"""
    credentials = session.get('google_credentials')
    if credentials:
        return 'Successfully authenticated with Google!'
    return 'No credentials found', 401

def get_google_credentials():
    """Get Google credentials from session"""
    credentials_info = session.get('google_credentials')
    if credentials_info:
        return Credentials(
            token=credentials_info['token'],
            refresh_token=credentials_info['refresh_token'],
            token_uri=credentials_info['token_uri'],
            client_id=credentials_info['client_id'],
            client_secret=credentials_info['client_secret'],
            scopes=credentials_info['scopes']
        )
    return None

if __name__ == '__main__':
    app.run(port=5006, debug=True)


