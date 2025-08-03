

# Telegram OAuth2 Integration Guide

This guide explains how to set up Telegram OAuth2 authentication for the AI Backlog Assistant.

## Overview

Telegram OAuth2 allows users to authenticate with their Telegram accounts to link them with the AI Backlog Assistant platform. This enables:

1. Telegram notifications
2. Account linking between Telegram and the web platform
3. Secure authentication using Telegram credentials

## Setup Instructions

### 1. Create a Telegram Bot

1. Open Telegram and search for the `@BotFather` bot
2. Create a new bot using the `/newbot` command
3. Follow the instructions to set up your bot
4. Note down the bot token (this will be used as the client secret)

### 2. Set up Telegram Login

1. Go to the [Telegram Login Widget](https://my.telegram.org/auth) page
2. Log in with your Telegram account
3. Create a new application:
   - App title: AI Backlog Assistant
   - App short name: ai_backlog
   - URL: http://localhost:5000 (or your production domain)
   - Platform: Web
4. Note down the Client ID and Client Secret

### 3. Configure Environment Variables

Add the following environment variables to your `.env` file:

```env
TELEGRAM_CLIENT_ID=your_telegram_client_id
TELEGRAM_CLIENT_SECRET=your_telegram_client_secret
TELEGRAM_REDIRECT_URI=http://localhost:5000/auth/telegram/callback
```

### 4. Update Configuration

Ensure your web server configuration includes the Telegram OAuth2 settings:

```python
app.config['TELEGRAM_CLIENT_ID'] = os.getenv('TELEGRAM_CLIENT_ID')
app.config['TELEGRAM_CLIENT_SECRET'] = os.getenv('TELEGRAM_CLIENT_SECRET')
```

### 5. Register the Telegram OAuth Provider

Add the Telegram OAuth provider to your Authlib configuration:

```python
telegram = oauth.register(
    name='telegram',
    client_id=app.config['TELEGRAM_CLIENT_ID'],
    client_secret=app.config['TELEGRAM_CLIENT_SECRET'],
    authorize_url='https://oauth.telegram.org/auth',
    authorize_params=None,
    access_token_url='https://oauth.telegram.org/token',
    access_token_params=None,
    api_base_url='https://api.telegram.org/',
    client_kwargs={'scope': 'profile'},
)
```

### 6. Add Authentication Routes

Add the following routes to handle Telegram authentication:

```python
@app.route('/auth/telegram')
def telegram_login():
    """Telegram login"""
    redirect_uri = url_for('telegram_auth', _external=True)
    return telegram.authorize_redirect(redirect_uri)

@app.route('/auth/telegram/callback')
def telegram_auth():
    """Telegram auth callback"""
    token = telegram.authorize_access_token()
    resp = telegram.get('userinfo')
    user_data = resp.json()

    # Telegram user info structure
    telegram_id = str(user_data.get('id'))
    username = user_data.get('username') or f"telegram_{telegram_id}"
    email = user_data.get('email') or f"{telegram_id}@telegram.user"

    # Find or create user
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User.query.filter_by(email=email).first()

    if not user:
        # Create new user
        user = User(
            username=username,
            email=email,
            telegram_id=telegram_id
        )
        db.session.add(user)
        db.session.commit()
    else:
        # Update existing user
        user.telegram_id = telegram_id
        user.username = username
        db.session.commit()

    login_user(user)
    return redirect(url_for('index'))
```

### 7. Update User Interface

Add a Telegram connection button to your settings page:

```html
<div class="card mt-4">
    <div class="card-body">
        <h5 class="card-title">Telegram Integration</h5>
        {% if not current_user.telegram_id %}
        <div class="alert alert-info">
            Telegram is not connected.
        </div>
        <a href="{{ url_for('telegram_login') }}" class="btn btn-primary">
            <i class="bi bi-telegram"></i> Connect Telegram Account
        </a>
        {% else %}
        <div class="alert alert-success">
            Telegram is connected.
        </div>
        <div class="mt-3">
            <h6>Telegram Notifications</h6>
            <div class="text-muted">
                Status: Connected
            </div>
        </div>
        {% endif %}
    </div>
</div>
```

## Testing

1. Start your web server: `python app.py`
2. Navigate to the settings page
3. Click "Connect Telegram Account"
4. Authorize the application in Telegram
5. You should be redirected back to the application and logged in

## Troubleshooting

### Common Issues

1. **Redirect URI mismatch**: Ensure the redirect URI in your Telegram app settings matches the one in your environment variables
2. **Invalid client credentials**: Double-check your client ID and secret
3. **Network issues**: Ensure your server can access Telegram's OAuth endpoints

### Debugging Tips

- Check the browser console for JavaScript errors
- Check your server logs for error messages
- Use a tool like Postman to test the Telegram API endpoints manually

## Security Considerations

1. **Secure your client secret**: Never expose your Telegram client secret in client-side code
2. **Use HTTPS**: Always use HTTPS for production environments
3. **Validate tokens**: Ensure you properly validate access tokens from Telegram
4. **Rate limiting**: Implement rate limiting to prevent abuse

## Additional Resources

- [Telegram Login Documentation](https://core.telegram.org/widgets/login)
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Authlib Documentation](https://authlib.org/)

