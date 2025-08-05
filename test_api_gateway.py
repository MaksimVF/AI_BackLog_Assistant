




import os
import sys
import uuid
import json
import requests
import threading
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from web_server.app import app, db
from web_server.models import User

def test_api_gateway():
    """Test the API Gateway functionality"""

    with app.app_context():
        # Create a test user (check if exists first)
        test_user = User.query.filter_by(email="test_api@example.com").first()
        if not test_user:
            user_id = str(uuid.uuid4())
            test_user = User(
                id=user_id,
                username="test_api_user",
                email="test_api@example.com"
            )
            test_user.set_password("test_password")
            db.session.add(test_user)
            db.session.commit()
            print(f"Created test user: {user_id}")
        else:
            user_id = test_user.id
            print(f"Using existing test user: {user_id}")

        # Start Flask app in a separate thread
        def run_flask():
            app.run(port=5003, debug=False)

        thread = threading.Thread(target=run_flask)
        thread.daemon = True
        thread.start()

        # Wait for server to start
        time.sleep(2)

        # Test login
        print("--- Testing Login ---")
        login_response = requests.post(
            "http://127.0.0.1:5003/api/v1/auth/login",
            json={"email": "test_api@example.com", "password": "test_password"}
        )
        print(f"Login: {login_response.status_code}")
        if login_response.status_code == 200:
            login_data = login_response.json()
            access_token = login_data.get('access_token')
            print(f"Access token: {access_token[:20]}...")

            # Test protected route
            print("--- Testing Protected Route ---")
            headers = {"Authorization": f"Bearer {access_token}"}
            me_response = requests.get(
                "http://127.0.0.1:5003/api/v1/auth/me",
                headers=headers
            )
            print(f"Me endpoint: {me_response.status_code}")
            print(f"Response: {me_response.text}")

            # Test document endpoint
            print("--- Testing Document Endpoint ---")
            doc_response = requests.get(
                "http://127.0.0.1:5003/api/v1/documents",
                headers=headers
            )
            print(f"Documents: {doc_response.status_code}")
            print(f"Response: {doc_response.text}")

        else:
            print(f"Error: {login_response.text}")

        # Stop the server (in a real test, we'd do this more gracefully)
        # For now, we'll just let the daemon thread exit when the script ends

if __name__ == "__main__":
    test_api_gateway()


