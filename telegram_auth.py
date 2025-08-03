
"""
Telegram OAuth2 Authentication for AI Backlog Assistant
"""

import os
import requests
from flask import Flask, redirect, request, session, url_for, jsonify
from authlib.integrations.flask_client import OAuth

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Telegram OAuth2 configuration
TELEGRAM_CLIENT_ID = os.getenv('TELEGRAM_CLIENT_ID', 'your_telegram_client_id')
TELEGRAM_CLIENT_SECRET = os.getenv('TELEGRAM_CLIENT_SECRET', 'your_telegram_client_secret')
TELEGRAM_REDIRECT_URI = os.getenv('TELEGRAM_REDIRECT_URI', 'http://localhost:50133/telegram/callback')

# Telegram OAuth2 endpoints
TELEGRAM_AUTH_URL = 'https://oauth.telegram.org/auth'
TELEGRAM_TOKEN_URL = 'https://oauth.telegram.org/token'
TELEGRAM_API_URL = 'https://api.telegram.org'

# Initialize OAuth
oauth = OAuth(app)

# Register Telegram OAuth provider
telegram = oauth.register(
    name='telegram',
    client_id=TELEGRAM_CLIENT_ID,
    client_secret=TELEGRAM_CLIENT_SECRET,
    authorize_url=TELEGRAM_AUTH_URL,
    authorize_params=None,
    access_token_url=TELEGRAM_TOKEN_URL,
    access_token_params=None,
    api_base_url=TELEGRAM_API_URL,
    client_kwargs={'scope': 'profile'},
)

@app.route('/telegram/login')
def telegram_login():
    """Redirect user to Telegram for authorization"""
    redirect_uri = url_for('telegram_callback', _external=True)
    auth_url = (
        f'{TELEGRAM_AUTH_URL}'
        f'?client_id={TELEGRAM_CLIENT_ID}'
        f'&redirect_uri={redirect_uri}'
        f'&scope=profile'
        f'&response_type=code'
    )
    return redirect(auth_url)

@app.route('/telegram/callback')
def telegram_callback():
    """Handle Telegram OAuth2 callback"""
    code = request.args.get('code')

    if not code:
        return 'Authorization code not provided', 400

    # Exchange authorization code for access token
    token_url = TELEGRAM_TOKEN_URL
    payload = {
        'grant_type': 'authorization_code',
        'client_id': TELEGRAM_CLIENT_ID,
        'client_secret': TELEGRAM_CLIENT_SECRET,
        'code': code,
        'redirect_uri': TELEGRAM_REDIRECT_URI
    }

    response = requests.post(token_url, data=payload)
    data = response.json()

    if 'access_token' not in data:
        return f'Telegram authentication failed: {data}', 401

    access_token = data['access_token']

    # Get user information from Telegram
    user_info_url = f'{TELEGRAM_API_URL}/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_response = requests.get(user_info_url, headers=headers)
    user_data = user_response.json()

    if 'id' not in user_data:
        return 'Failed to get Telegram user information', 401

    # Store Telegram user information in session
    session['telegram_user'] = {
        'id': user_data['id'],
        'username': user_data.get('username'),
        'first_name': user_data.get('first_name'),
        'last_name': user_data.get('last_name'),
        'access_token': access_token
    }

    return redirect(url_for('telegram_success'))

@app.route('/telegram/success')
def telegram_success():
    """Show successful Telegram authentication"""
    telegram_user = session.get('telegram_user')
    if telegram_user:
        return f'Successfully authenticated with Telegram! User ID: {telegram_user["id"]}'
    return 'No Telegram user information found', 401

@app.route('/telegram/user')
def telegram_user():
    """Get current Telegram user information"""
    telegram_user = session.get('telegram_user')
    if telegram_user:
        return jsonify(telegram_user)
    return jsonify({'error': 'Not authenticated with Telegram'}), 401

if __name__ == '__main__':
    app.run(port=50133, debug=True)
