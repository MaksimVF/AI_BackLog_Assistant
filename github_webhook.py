

from flask import Flask, request, jsonify
import hashlib
import hmac
import json

app = Flask(__name__)

# GitHub webhook secret (should match what you set in GitHub)
GITHUB_WEBHOOK_SECRET = 'your_webhook_secret'

def verify_signature(payload, signature, secret):
    """Verify the GitHub webhook signature"""
    hash_algorithm, github_signature = signature.split('=')
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_secret = bytes(secret, 'utf-8')
    encoded_payload = bytes(payload, 'utf-8')

    if not algorithm:
        return False

    mac = hmac.new(encoded_secret, encoded_payload, algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)

@app.route('/github/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events"""
    signature = request.headers.get('X-Hub-Signature')
    event = request.headers.get('X-GitHub-Event')

    if not verify_signature(request.data, signature, GITHUB_WEBHOOK_SECRET):
        return jsonify({'error': 'Invalid signature'}), 401

    payload = request.json

    # Process different GitHub events
    if event == 'issues':
        handle_issue_event(payload)
    elif event == 'pull_request':
        handle_pull_request_event(payload)
    elif event == 'push':
        handle_push_event(payload)

    return jsonify({'status': 'success'}), 200

def handle_issue_event(payload):
    """Process GitHub issue events"""
    action = payload.get('action')
    issue = payload.get('issue')

    print(f"Issue event received: {action}")
    print(f"Issue title: {issue.get('title')}")
    print(f"Issue body: {issue.get('body')}")

    # Here you would integrate with your agent system
    # For example: CategorizationAgent.process_issue(issue)

def handle_pull_request_event(payload):
    """Process GitHub pull request events"""
    action = payload.get('action')
    pr = payload.get('pull_request')

    print(f"PR event received: {action}")
    print(f"PR title: {pr.get('title')}")
    print(f"PR body: {pr.get('body')}")

    # Here you would integrate with your agent system
    # For example: ReflectionAgent.analyze_pr(pr)

def handle_push_event(payload):
    """Process GitHub push events"""
    ref = payload.get('ref')
    commits = payload.get('commits')

    print(f"Push event received to {ref}")
    print(f"Number of commits: {len(commits)}")

    # Here you would integrate with your agent system
    # For example: EffortEstimatorAgent.estimate_commits(commits)

if __name__ == '__main__':
    app.run(port=5001, debug=True)

