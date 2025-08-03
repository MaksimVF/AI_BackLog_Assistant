



from flask import Flask, request, jsonify
import hashlib
import hmac
import json

app = Flask(__name__)

# Bitbucket webhook secret (should match what you set in Bitbucket)
BITBUCKET_WEBHOOK_SECRET = 'your_webhook_secret'

def verify_signature(payload, signature, secret):
    """Verify the Bitbucket webhook signature"""
    mac = hmac.new(secret.encode(), payload, hashlib.sha256)
    expected_signature = mac.hexdigest()

    return hmac.compare_digest(expected_signature, signature)

@app.route('/bitbucket/webhook', methods=['POST'])
def bitbucket_webhook():
    """Handle Bitbucket webhook events"""
    signature = request.headers.get('X-Hub-Signature')
    event = request.headers.get('X-Event-Key')

    if signature and not verify_signature(request.data, signature, BITBUCKET_WEBHOOK_SECRET):
        return jsonify({'error': 'Invalid signature'}), 401

    payload = request.json

    # Process different Bitbucket events
    if event == 'issue:created' or event == 'issue:updated':
        handle_issue_event(payload)
    elif event == 'pullrequest:created' or event == 'pullrequest:updated':
        handle_pull_request_event(payload)
    elif event == 'repo:push':
        handle_push_event(payload)

    return jsonify({'status': 'success'}), 200

def handle_issue_event(payload):
    """Process Bitbucket issue events"""
    issue = payload.get('issue', {})

    print(f"Issue event received: {payload.get('eventKey')}")
    print(f"Issue title: {issue.get('title')}")
    print(f"Issue content: {issue.get('content', {}).get('raw', '')}")

    # Here you would integrate with your agent system
    # For example: CategorizationAgent.process_issue(issue)

def handle_pull_request_event(payload):
    """Process Bitbucket pull request events"""
    pr = payload.get('pullrequest', {})

    print(f"PR event received: {payload.get('eventKey')}")
    print(f"PR title: {pr.get('title')}")
    print(f"PR description: {pr.get('description', '')}")

    # Here you would integrate with your agent system
    # For example: ReflectionAgent.analyze_pr(pr)

def handle_push_event(payload):
    """Process Bitbucket push events"""
    push = payload.get('push', {})
    changes = push.get('changes', [])

    print(f"Push event received: {payload.get('eventKey')}")
    print(f"Number of changes: {len(changes)}")

    # Here you would integrate with your agent system
    # For example: EffortEstimatorAgent.estimate_commits(changes)

if __name__ == '__main__':
    app.run(port=5005, debug=True)



