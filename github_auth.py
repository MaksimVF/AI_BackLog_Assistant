
import requests
from flask import Flask, redirect, request, session, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# GitHub OAuth2 configuration
GITHUB_CLIENT_ID = 'your_client_id'
GITHUB_CLIENT_SECRET = 'your_client_secret'
GITHUB_REDIRECT_URI = 'http://localhost:5000/github/callback'

# Scopes required for our integration
GITHUB_SCOPES = 'repo,read:org,workflow,admin:repo_hook'

@app.route('/github/login')
def github_login():
    """Redirect user to GitHub for authorization"""
    auth_url = (
        'https://github.com/login/oauth/authorize'
        f'?client_id={GITHUB_CLIENT_ID}'
        f'&redirect_uri={GITHUB_REDIRECT_URI}'
        f'&scope={GITHUB_SCOPES}'
    )
    return redirect(auth_url)

@app.route('/github/callback')
def github_callback():
    """Handle GitHub OAuth2 callback"""
    code = request.args.get('code')

    # Exchange authorization code for access token
    token_url = 'https://github.com/login/oauth/access_token'
    payload = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': GITHUB_REDIRECT_URI
    }
    headers = {'Accept': 'application/json'}

    response = requests.post(token_url, json=payload, headers=headers)
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        session['github_token'] = access_token
        return redirect(url_for('github_success'))
    else:
        return 'GitHub authentication failed', 401

@app.route('/github/success')
def github_success():
    """Show successful authentication"""
    token = session.get('github_token')
    if token:
        return f'Successfully authenticated with GitHub! Token: {token}'
    return 'No token found', 401

if __name__ == '__main__':
    app.run(debug=True)
