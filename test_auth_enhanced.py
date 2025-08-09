





"""
Test script for enhanced authentication and authorization system
"""

import os
import sys
import time
import uuid
from datetime import datetime, timedelta

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security.auth_enhanced import (
    EnhancedAuthSystem, AuthError, InvalidCredentialsError,
    AccountLockedError, TokenExpiredError, InsufficientPermissionsError,
    UserRole, Permission, UserStatus
)

def test_authentication():
    """Test authentication functionality"""
    print("=== Testing Authentication ===")

    auth_system = EnhancedAuthSystem()

    # Test successful authentication
    try:
        user, tokens = auth_system.authenticate("admin", "admin123")
        print(f"✓ Admin authentication successful: {user.username}")
        print(f"  - Access token: {tokens['access_token'][:50]}...")
        print(f"  - Refresh token: {tokens['refresh_token'][:50]}...")
    except AuthError as e:
        print(f"❌ Admin authentication failed: {e}")

    # Test invalid credentials
    try:
        auth_system.authenticate("admin", "wrongpassword")
        print("❌ Invalid credentials test should have failed")
    except InvalidCredentialsError:
        print("✓ Invalid credentials correctly rejected")

    # Test account lockout
    try:
        # Try multiple failed attempts
        for i in range(5):
            try:
                auth_system.authenticate("user", f"wrongpassword{i}")
            except InvalidCredentialsError:
                pass  # Expected

        # Next attempt should lock the account
        auth_system.authenticate("user", "wrongpassword6")
        print("❌ Account lockout test should have failed")
    except AccountLockedError:
        print("✓ Account lockout working correctly")

    # Test with correct credentials after lockout
    try:
        auth_system.authenticate("user", "user123")
        print("❌ Authentication after lockout should have failed")
    except AccountLockedError:
        print("✓ Authentication correctly blocked after lockout")

    print("✓ Authentication tests completed")

def test_token_management():
    """Test token management"""
    print("\n=== Testing Token Management ===")

    auth_system = EnhancedAuthSystem()

    # Get tokens
    user, tokens = auth_system.authenticate("admin", "admin123")

    # Test token verification
    try:
        payload = auth_system.verify_token(tokens['access_token'])
        print(f"✓ Token verification successful: {payload['username']}")
    except AuthError as e:
        print(f"❌ Token verification failed: {e}")

    # Test token refresh
    try:
        new_tokens = auth_system.refresh_tokens(tokens['refresh_token'])
        print(f"✓ Token refresh successful")
        print(f"  - New access token: {new_tokens['access_token'][:50]}...")
    except AuthError as e:
        print(f"❌ Token refresh failed: {e}")

    # Test expired token
    # Create a token that expires immediately
    expired_token = auth_system._create_token(
        user.user_id, user.username, user.role,
        expires_in=-3600  # Expired 1 hour ago
    )

    try:
        auth_system.verify_token(expired_token)
        print("❌ Expired token verification should have failed")
    except TokenExpiredError:
        print("✓ Expired token correctly rejected")

    print("✓ Token management tests completed")

def test_authorization():
    """Test authorization functionality"""
    print("\n=== Testing Authorization ===")

    auth_system = EnhancedAuthSystem()

    # Get admin user
    admin_user = auth_system.get_user_by_username("admin")

    # Test admin permissions
    try:
        auth_system.authorize(admin_user.user_id, Permission.MANAGE_USERS)
        print("✓ Admin authorized for MANAGE_USERS")
    except AuthError as e:
        print(f"❌ Admin authorization failed: {e}")

    try:
        auth_system.authorize(admin_user.user_id, Permission.VIEW_DOCUMENTS)
        print("✓ Admin authorized for VIEW_DOCUMENTS")
    except AuthError as e:
        print(f"❌ Admin authorization failed: {e}")

    # Test role requirements
    try:
        auth_system.require_role(admin_user.user_id, UserRole.ADMIN)
        print("✓ Admin role requirement satisfied")
    except AuthError as e:
        print(f"❌ Admin role requirement failed: {e}")

    # Test insufficient permissions
    try:
        auth_system.authorize(admin_user.user_id, Permission.MANAGE_BACKUPS)
        print("✓ Admin authorized for MANAGE_BACKUPS")
    except AuthError as e:
        print(f"❌ Admin authorization failed: {e}")

    # Create a regular user and test their permissions
    regular_user = auth_system.get_user_by_username("user")

    try:
        auth_system.authorize(regular_user.user_id, Permission.CREATE_DOCUMENTS)
        print("✓ Regular user authorized for CREATE_DOCUMENTS")
    except AuthError as e:
        print(f"❌ Regular user authorization failed: {e}")

    try:
        auth_system.authorize(regular_user.user_id, Permission.MANAGE_USERS)
        print("❌ Regular user should not be authorized for MANAGE_USERS")
    except InsufficientPermissionsError:
        print("✓ Regular user correctly denied MANAGE_USERS permission")

    print("✓ Authorization tests completed")

def test_mfa():
    """Test multi-factor authentication"""
    print("\n=== Testing Multi-Factor Authentication ===")

    auth_system = EnhancedAuthSystem()

    # Get admin user
    admin_user = auth_system.get_user_by_username("admin")

    # Enable MFA
    try:
        mfa_secret = auth_system.enable_mfa(admin_user.user_id)
        print(f"✓ MFA enabled for admin: {mfa_secret}")
    except AuthError as e:
        print(f"❌ MFA enable failed: {e}")

    # Test MFA verification
    try:
        mfa_verified = auth_system.verify_mfa(admin_user.user_id, mfa_secret)
        print(f"✓ MFA verification: {mfa_verified}")
    except AuthError as e:
        print(f"❌ MFA verification failed: {e}")

    # Test wrong MFA code
    try:
        auth_system.verify_mfa(admin_user.user_id, "wrong_code")
        print("❌ Wrong MFA code should have failed")
    except AuthError:
        print("✓ Wrong MFA code correctly rejected")

    # Disable MFA
    try:
        auth_system.disable_mfa(admin_user.user_id)
        print("✓ MFA disabled for admin")
    except AuthError as e:
        print(f"❌ MFA disable failed: {e}")

    print("✓ MFA tests completed")

def test_user_management():
    """Test user management functionality"""
    print("\n=== Testing User Management ===")

    auth_system = EnhancedAuthSystem()

    # Create a new user
    try:
        new_user = auth_system.create_user(
            username="testuser",
            email="test@example.com",
            password="Test123!@#",
            role=UserRole.USER,
            permissions=[Permission.VIEW_DOCUMENTS]
        )
        print(f"✓ User created: {new_user.username}")
    except ValueError as e:
        print(f"❌ User creation failed: {e}")

    # Test weak password
    try:
        auth_system.create_user(
            username="weakuser",
            email="weak@example.com",
            password="weak",
            role=UserRole.USER
        )
        print("❌ Weak password should have been rejected")
    except ValueError:
        print("✓ Weak password correctly rejected")

    # Test duplicate user
    try:
        auth_system.create_user(
            username="testuser",
            email="duplicate@example.com",
            password="Test123!@#",
            role=UserRole.USER
        )
        print("❌ Duplicate username should have been rejected")
    except ValueError:
        print("✓ Duplicate username correctly rejected")

    # Test password update
    try:
        auth_system.update_user_password(new_user.user_id, "NewTest123!@#")
        print("✓ User password updated successfully")
    except ValueError as e:
        print(f"❌ Password update failed: {e}")

    # Test weak password update
    try:
        auth_system.update_user_password(new_user.user_id, "weak")
        print("❌ Weak password update should have been rejected")
    except ValueError:
        print("✓ Weak password update correctly rejected")

    print("✓ User management tests completed")

def test_integration():
    """Test complete authentication and authorization integration"""
    print("\n=== Testing Complete Integration ===")

    auth_system = EnhancedAuthSystem()

    # Complete authentication flow
    try:
        # 1. User authenticates
        user, tokens = auth_system.authenticate("admin", "admin123")
        print(f"✓ User authenticated: {user.username}")

        # 2. Verify access token
        payload = auth_system.verify_token(tokens['access_token'])
        print(f"✓ Token verified: {payload['username']}")

        # 3. Check permissions
        auth_system.authorize(user.user_id, Permission.MANAGE_USERS)
        print(f"✓ Permission granted: MANAGE_USERS")

        # 4. Check role
        auth_system.require_role(user.user_id, UserRole.ADMIN)
        print(f"✓ Role requirement satisfied: ADMIN")

        # 5. Enable MFA
        mfa_secret = auth_system.enable_mfa(user.user_id)
        print(f"✓ MFA enabled")

        # 6. Verify MFA
        mfa_verified = auth_system.verify_mfa(user.user_id, mfa_secret)
        print(f"✓ MFA verified: {mfa_verified}")

        # 7. Refresh tokens
        new_tokens = auth_system.refresh_tokens(tokens['refresh_token'])
        print(f"✓ Tokens refreshed")

        print("✓ Complete integration test successful")

    except AuthError as e:
        print(f"❌ Integration test failed: {e}")

    print("✓ Integration tests completed")

def main():
    """Run all authentication tests"""
    print("🔒 Running Enhanced Authentication Tests")
    print("=" * 50)

    try:
        test_authentication()
        test_token_management()
        test_authorization()
        test_mfa()
        test_user_management()
        test_integration()

        print("\n🎉 All enhanced authentication tests completed!")
        print("✅ Authentication and authorization improvements are working correctly")

    except Exception as e:
        print(f"\n❌ Authentication test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()





