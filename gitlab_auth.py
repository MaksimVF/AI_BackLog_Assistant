

import requests
from flask import Flask, redirect, request, session, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# GitLab OAuth2 configuration
GITLAB_CLIENT_ID = 'your_client_id'
GITLAB_CLIENT_SECRET = 'your_client_secret'
GITLAB_REDIRECT_URI = 'http://localhost:5002/gitlab/callback'

# Scopes required for our integration
GITLAB_SCOPES = 'api read_repository write_repository read_user'

@app.route('/gitlab/login')
def gitlab_login():
    """Redirect user to GitLab for authorization"""
    auth_url = (
        'https://gitlab.com/oauth/authorize'
        f'?client_id={GITLAB_CLIENT_ID}'
        f'&redirect_uri={GITLAB_REDIRECT_URI}'
        f'&response_type=code'
        f'&scope={GITLAB_SCOPES}'
    )
    return redirect(auth_url)

@app.route('/gitlab/callback')
def gitlab_callback():
    """Handle GitLab OAuth2 callback"""
    code = request.args.get('code')

    # Exchange authorization code for access token
    token_url = 'https://gitlab.com/oauth/token'
    payload = {
        'client_id': GITLAB_CLIENT_ID,
        'client_secret': GITLAB_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': GITLAB_REDIRECT_URI
    }

    response = requests.post(token_url, data=payload)
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        session['gitlab_token'] = access_token
        return redirect(url_for('gitlab_success'))
    else:
        return 'GitLab authentication failed', 401

@app.route('/gitlab/success')
def gitlab_success():
    """Show successful authentication"""
    token = session.get('gitlab_token')
    if token:
        return f'Successfully authenticated with GitLab! Token: {token}'
    return 'No token found', 401

if __name__ == '__main__':
    app.run(port=5002, debug=True)

