


from flask import Flask, request, jsonify
import hashlib
import hmac
import json

app = Flask(__name__)

# GitLab webhook secret (should match what you set in GitLab)
GITLAB_WEBHOOK_SECRET = 'your_webhook_secret'

def verify_signature(payload, signature, secret):
    """Verify the GitLab webhook signature"""
    mac = hmac.new(secret.encode(), payload, hashlib.sha256)
    expected_signature = 'sha256=' + mac.hexdigest()

    return hmac.compare_digest(expected_signature, signature)

@app.route('/gitlab/webhook', methods=['POST'])
def gitlab_webhook():
    """Handle GitLab webhook events"""
    signature = request.headers.get('X-Gitlab-Token')
    event = request.headers.get('X-Gitlab-Event')

    # For GitLab, we typically use a simple token verification
    if signature != GITLAB_WEBHOOK_SECRET:
        return jsonify({'error': 'Invalid token'}), 401

    payload = request.json

    # Process different GitLab events
    if event == 'Issue Hook':
        handle_issue_event(payload)
    elif event == 'Merge Request Hook':
        handle_merge_request_event(payload)
    elif event == 'Push Hook':
        handle_push_event(payload)

    return jsonify({'status': 'success'}), 200

def handle_issue_event(payload):
    """Process GitLab issue events"""
    object_kind = payload.get('object_kind')
    issue = payload.get('issue', {})

    print(f"Issue event received: {object_kind}")
    print(f"Issue title: {issue.get('title')}")
    print(f"Issue description: {issue.get('description')}")

    # Here you would integrate with your agent system
    # For example: CategorizationAgent.process_issue(issue)

def handle_merge_request_event(payload):
    """Process GitLab merge request events"""
    object_kind = payload.get('object_kind')
    mr = payload.get('merge_request', {})

    print(f"MR event received: {object_kind}")
    print(f"MR title: {mr.get('title')}")
    print(f"MR description: {mr.get('description')}")

    # Here you would integrate with your agent system
    # For example: ReflectionAgent.analyze_mr(mr)

def handle_push_event(payload):
    """Process GitLab push events"""
    ref = payload.get('ref')
    commits = payload.get('commits', [])

    print(f"Push event received to {ref}")
    print(f"Number of commits: {len(commits)}")

    # Here you would integrate with your agent system
    # For example: EffortEstimatorAgent.estimate_commits(commits)

if __name__ == '__main__':
    app.run(port=5003, debug=True)


