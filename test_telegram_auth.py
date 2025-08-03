

"""
Test script for Telegram OAuth2 authentication
"""

import os
import sys
import requests
from flask import Flask, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the web server app
from web_server.app import app as web_app, db, User

def test_telegram_auth_setup():
    """Test that Telegram OAuth2 is properly configured"""
    print("Testing Telegram OAuth2 setup...")

    # Check if Telegram client credentials are configured
    telegram_client_id = web_app.config.get('TELEGRAM_CLIENT_ID')
    telegram_client_secret = web_app.config.get('TELEGRAM_CLIENT_SECRET')

    if not telegram_client_id or not telegram_client_secret:
        print("❌ Telegram client credentials not configured")
        return False

    print("✅ Telegram client credentials configured")

    # Check if OAuth provider is registered
    if 'telegram' not in web_app.extensions['auth']:
        print("❌ Telegram OAuth provider not registered")
        return False

    print("✅ Telegram OAuth provider registered")

    # Check if routes exist
    with web_app.test_client() as client:
        # Test login route
        response = client.get('/auth/telegram')
        if response.status_code != 302:  # Should redirect
            print("❌ Telegram login route not working")
            return False

        print("✅ Telegram login route working")

        # Test callback route
        response = client.get('/auth/telegram/callback')
        if response.status_code != 400:  # Should fail without code parameter
            print("❌ Telegram callback route not working")
            return False

        print("✅ Telegram callback route working")

    print("✅ All Telegram OAuth2 setup tests passed")
    return True

def test_user_model():
    """Test that User model supports Telegram integration"""
    print("Testing User model for Telegram support...")

    # Check if telegram_id field exists
    if not hasattr(User, 'telegram_id'):
        print("❌ User model missing telegram_id field")
        return False

    print("✅ User model has telegram_id field")

    # Test creating a user with Telegram ID
    with web_app.app_context():
        # Create a test user
        test_user = User(
            username='test_telegram_user',
            email='test_telegram@example.com',
            telegram_id='123456789'
        )

        try:
            db.session.add(test_user)
            db.session.commit()
            print("✅ Successfully created user with Telegram ID")
            return True
        except Exception as e:
            print(f"❌ Failed to create user with Telegram ID: {e}")
            db.session.rollback()
            return False
        finally:
            # Clean up
            try:
                db.session.delete(test_user)
                db.session.commit()
            except:
                db.session.rollback()

if __name__ == '__main__':
    print("Running Telegram OAuth2 integration tests...")
    print("=" * 50)

    # Set up test environment
    web_app.config['TESTING'] = True
    web_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    web_app.config['WTF_CSRF_ENABLED'] = False

    with web_app.app_context():
        db.create_all()

        # Run tests
        setup_ok = test_telegram_auth_setup()
        user_model_ok = test_user_model()

        if setup_ok and user_model_ok:
            print("\n🎉 All Telegram OAuth2 tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some Telegram OAuth2 tests failed!")
            sys.exit(1)

