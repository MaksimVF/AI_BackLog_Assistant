


# Bitbucket Integration Setup Guide

## 1. Create a Bitbucket OAuth Consumer

1. Go to your Bitbucket account settings: https://bitbucket.org/account/user/{your_username}/app-passwords
2. Click "Create app password"
3. Set permissions: Repositories (Read), Issues (Read/Write), Pull requests (Read/Write)
4. Copy the generated password

For full OAuth2 flow:
1. Go to your Bitbucket workspace settings: https://bitbucket.org/{workspace}/workspace/settings/oauth-consumers
2. Click "Add consumer"
3. Fill in the form:
   - Name: AI Backlog Assistant
   - Callback URL: http://localhost:5004/bitbucket/callback
   - Permissions: Repository (read), Issue (read/write), Pull request (read/write)
4. Click "Save"
5. Copy the Key and Secret

## 2. Create a Bitbucket Webhook

1. Go to your repository on Bitbucket
2. Click Repository settings > Webhooks > Add webhook
3. Set the URL to: http://localhost:5005/bitbucket/webhook
4. Choose triggers: Repository push, Issue created/updated, Pull request created/updated
5. Click "Save"

## 3. Environment Variables

Create a `.env` file with these variables:

```
BITBUCKET_CLIENT_ID=your_client_id
BITBUCKET_CLIENT_SECRET=your_client_secret
BITBUCKET_WEBHOOK_SECRET=your_webhook_secret
```

## 4. Running the Services

1. Start the OAuth server:
   ```bash
   python bitbucket_auth.py
   ```

2. Start the webhook server:
   ```bash
   python bitbucket_webhook.py
   ```

3. Test the integration:
   - Open http://localhost:5004/bitbucket/login to authenticate
   - Create/modify issues/PRs in your Bitbucket repo to trigger webhooks

## 5. Integrating with Your Main Application

You can now integrate the BitbucketConnectorAgent with your existing agent system as shown in the multi_platform_integration.py example.


