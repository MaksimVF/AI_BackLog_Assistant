
# GitHub Integration Setup Guide

## 1. Create a GitHub OAuth Application

1. Go to your GitHub account settings: https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in the form:
   - Application name: AI Backlog Assistant
   - Homepage URL: http://localhost:5000
   - Authorization callback URL: http://localhost:5000/github/callback
4. Click "Register application"
5. Copy the Client ID and Client Secret to your `.env` file

## 2. Create a GitHub Webhook

1. Go to your repository on GitHub
2. Click Settings > Webhooks > Add webhook
3. Set the Payload URL to: http://localhost:5001/github/webhook
4. Set Content type to: application/json
5. Set Secret to: your_webhook_secret (same as in github_webhook.py)
6. Choose "Send me everything" or select specific events
7. Click "Add webhook"

## 3. Environment Variables

Create a `.env` file with these variables:

```
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
GITHUB_WEBHOOK_SECRET=your_webhook_secret
```

## 4. Running the Services

1. Start the OAuth server:
   ```bash
   python github_auth.py
   ```

2. Start the webhook server:
   ```bash
   python github_webhook.py
   ```

3. Test the integration:
   - Open http://localhost:5000/github/login to authenticate
   - Create/modify issues/PRs in your GitHub repo to trigger webhooks

## 5. Integrating with Your Main Application

You can now integrate the GitHubConnectorAgent with your existing agent system as shown in the agent_integration.py example.
