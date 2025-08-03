


import requests
from flask import Flask, redirect, request, session, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Bitbucket OAuth2 configuration
BITBUCKET_CLIENT_ID = 'your_client_id'
BITBUCKET_CLIENT_SECRET = 'your_client_secret'
BITBUCKET_REDIRECT_URI = 'http://localhost:5004/bitbucket/callback'

# Scopes required for our integration
BITBUCKET_SCOPES = 'repository issue pullrequest'

@app.route('/bitbucket/login')
def bitbucket_login():
    """Redirect user to Bitbucket for authorization"""
    auth_url = (
        'https://bitbucket.org/site/oauth2/authorize'
        f'?client_id={BITBUCKET_CLIENT_ID}'
        f'&response_type=code'
        f'&redirect_uri={BITBUCKET_REDIRECT_URI}'
    )
    return redirect(auth_url)

@app.route('/bitbucket/callback')
def bitbucket_callback():
    """Handle Bitbucket OAuth2 callback"""
    code = request.args.get('code')

    # Exchange authorization code for access token
    token_url = 'https://bitbucket.org/site/oauth2/access_token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code
    }
    auth = (BITBUCKET_CLIENT_ID, BITBUCKET_CLIENT_SECRET)

    response = requests.post(token_url, data=payload, auth=auth)
    data = response.json()

    if 'access_token' in data:
        access_token = data['access_token']
        session['bitbucket_token'] = access_token
        return redirect(url_for('bitbucket_success'))
    else:
        return 'Bitbucket authentication failed', 401

@app.route('/bitbucket/success')
def bitbucket_success():
    """Show successful authentication"""
    token = session.get('bitbucket_token')
    if token:
        return f'Successfully authenticated with Bitbucket! Token: {token}'
    return 'No token found', 401

if __name__ == '__main__':
    app.run(port=5004, debug=True)



