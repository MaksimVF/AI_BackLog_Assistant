

# GitLab Integration Setup Guide

## 1. Create a GitLab OAuth Application

1. Go to your GitLab account settings: https://gitlab.com/-/profile/applications
2. Click "New Application"
3. Fill in the form:
   - Name: AI Backlog Assistant
   - Redirect URI: http://localhost:5002/gitlab/callback
   - Scopes: api, read_repository, write_repository, read_user
4. Click "Save application"
5. Copy the Application ID and Secret to your `.env` file

## 2. Create a GitLab Webhook

1. Go to your project on GitLab
2. Click Settings > Webhooks
3. Set the URL to: http://localhost:5003/gitlab/webhook
4. Set Secret Token to: your_webhook_secret (same as in gitlab_webhook.py)
5. Choose triggers: Issues, Merge requests, Push events
6. Click "Add webhook"

## 3. Environment Variables

Create a `.env` file with these variables:

```
GITLAB_CLIENT_ID=your_client_id
GITLAB_CLIENT_SECRET=your_client_secret
GITLAB_WEBHOOK_SECRET=your_webhook_secret
```

## 4. Running the Services

1. Start the OAuth server:
   ```bash
   python gitlab_auth.py
   ```

2. Start the webhook server:
   ```bash
   python gitlab_webhook.py
   ```

3. Test the integration:
   - Open http://localhost:5002/gitlab/login to authenticate
   - Create/modify issues/MRs in your GitLab project to trigger webhooks

## 5. Integrating with Your Main Application

You can now integrate the GitLabConnectorAgent with your existing agent system as shown in the multi_platform_integration.py example.

