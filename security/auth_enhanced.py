




"""
Enhanced Authentication and Authorization System

This module provides comprehensive authentication and authorization features including:
1. Multi-factor authentication (MFA)
2. Role-based access control (RBAC)
3. Permission-based access control
4. Token management with refresh tokens
5. Password policies and account lockout
"""

import os
import time
import logging
import secrets
import uuid
import bcrypt
import jwt
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union, Tuple
from enum import Enum, auto
from dataclasses import dataclass, field
from fastapi import HTTPException, status
from pydantic import BaseModel

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AuthEnhanced")

class AuthError(Exception):
    """Base authentication error"""
    pass

class InvalidCredentialsError(AuthError):
    """Invalid credentials provided"""
    pass

class InsufficientPermissionsError(AuthError):
    """Insufficient permissions for operation"""
    pass

class AccountLockedError(AuthError):
    """Account is locked due to too many failed attempts"""
    pass

class MFARequiredError(AuthError):
    """Multi-factor authentication required"""
    pass

class TokenExpiredError(AuthError):
    """Token has expired"""
    pass

class UserRole(Enum):
    """User roles with hierarchical permissions"""
    ADMIN = auto()
    MANAGER = auto()
    USER = auto()
    GUEST = auto()

    def has_permission(self, required_role) -> bool:
        """Check if this role has the required permission"""
        return self.value >= required_role.value

class Permission(Enum):
    """System permissions"""
    # Admin permissions
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    MANAGE_SETTINGS = "manage_settings"

    # User permissions
    CREATE_DOCUMENTS = "create_documents"
    EDIT_DOCUMENTS = "edit_documents"
    DELETE_DOCUMENTS = "delete_documents"
    VIEW_DOCUMENTS = "view_documents"

    # Organization permissions
    MANAGE_ORGANIZATION = "manage_organization"
    INVITE_MEMBERS = "invite_members"
    REMOVE_MEMBERS = "remove_members"

    # System permissions
    VIEW_SYSTEM_STATUS = "view_system_status"
    MANAGE_BACKUPS = "manage_backups"

class UserStatus(Enum):
    """User account status"""
    ACTIVE = "active"
    LOCKED = "locked"
    PENDING = "pending"
    DISABLED = "disabled"

@dataclass
class User:
    """Enhanced user model with security features"""
    user_id: str
    username: str
    email: str
    password_hash: str
    role: UserRole
    status: UserStatus
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    failed_login_attempts: int = 0
    last_login: Optional[datetime] = None
    permissions: List[Permission] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def check_password(self, password: str) -> bool:
        """Check if password is correct"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions

    def has_role(self, role: UserRole) -> bool:
        """Check if user has specific role"""
        return self.role == role

    def is_locked(self) -> bool:
        """Check if account is locked"""
        return self.status == UserStatus.LOCKED

    def lock_account(self):
        """Lock the account"""
        self.status = UserStatus.LOCKED
        self.updated_at = datetime.utcnow()

    def unlock_account(self):
        """Unlock the account"""
        self.status = UserStatus.ACTIVE
        self.failed_login_attempts = 0
        self.updated_at = datetime.utcnow()

class AuthConfig:
    """Authentication configuration"""
    def __init__(
        self,
        jwt_secret: str = None,
        jwt_algorithm: str = "HS256",
        access_token_expiration: int = 3600,  # 1 hour
        refresh_token_expiration: int = 2592000,  # 30 days
        max_failed_attempts: int = 5,
        lockout_duration: int = 900,  # 15 minutes
        password_min_length: int = 8,
        password_require_uppercase: bool = True,
        password_require_numbers: bool = True,
        password_require_special: bool = True
    ):
        self.jwt_secret = jwt_secret or secrets.token_hex(32)
        self.jwt_algorithm = jwt_algorithm
        self.access_token_expiration = access_token_expiration
        self.refresh_token_expiration = refresh_token_expiration
        self.max_failed_attempts = max_failed_attempts
        self.lockout_duration = lockout_duration
        self.password_min_length = password_min_length
        self.password_require_uppercase = password_require_uppercase
        self.password_require_numbers = password_require_numbers
        self.password_require_special = password_require_special

class EnhancedAuthSystem:
    """Enhanced authentication and authorization system"""

    def __init__(self, config: AuthConfig = None):
        """Initialize the authentication system"""
        self.config = config or AuthConfig()
        self.users: Dict[str, User] = {}
        self.tokens: Dict[str, Dict[str, Any]] = {}
        self._initialize_default_users()

    def _initialize_default_users(self):
        """Initialize default users"""
        # Create admin user
        admin_user = User(
            user_id=str(uuid.uuid4()),
            username="admin",
            email="admin@example.com",
            password_hash=self._hash_password("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            permissions=[
                Permission.MANAGE_USERS,
                Permission.MANAGE_ROLES,
                Permission.VIEW_AUDIT_LOGS,
                Permission.MANAGE_SETTINGS,
                Permission.CREATE_DOCUMENTS,
                Permission.EDIT_DOCUMENTS,
                Permission.DELETE_DOCUMENTS,
                Permission.VIEW_DOCUMENTS,
                Permission.MANAGE_ORGANIZATION,
                Permission.INVITE_MEMBERS,
                Permission.REMOVE_MEMBERS,
                Permission.VIEW_SYSTEM_STATUS,
                Permission.MANAGE_BACKUPS
            ]
        )
        self.users[admin_user.user_id] = admin_user

        # Create regular user
        regular_user = User(
            user_id=str(uuid.uuid4()),
            username="user",
            email="user@example.com",
            password_hash=self._hash_password("user123"),
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            permissions=[
                Permission.CREATE_DOCUMENTS,
                Permission.EDIT_DOCUMENTS,
                Permission.VIEW_DOCUMENTS
            ]
        )
        self.users[regular_user.user_id] = regular_user

    def _hash_password(self, password: str) -> str:
        """Hash a password"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def _validate_password(self, password: str) -> bool:
        """Validate password against policy"""
        if len(password) < self.config.password_min_length:
            return False

        if self.config.password_require_uppercase and not any(c.isupper() for c in password):
            return False

        if self.config.password_require_numbers and not any(c.isdigit() for c in password):
            return False

        if self.config.password_require_special and not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            return False

        return True

    def authenticate(self, username: str, password: str) -> Tuple[User, Dict[str, str]]:
        """
        Authenticate a user and return tokens

        Args:
            username: Username or email
            password: Password

        Returns:
            Tuple of (user, tokens)

        Raises:
            AuthError: If authentication fails
        """
        # Find user by username or email
        user = None
        for u in self.users.values():
            if u.username == username or u.email == username:
                user = u
                break

        if not user:
            logger.warning(f"Authentication failed: user {username} not found")
            raise InvalidCredentialsError("Invalid username or password")

        # Check account status
        if user.is_locked():
            raise AccountLockedError("Account is locked due to too many failed attempts")

        # Check password
        if not user.check_password(password):
            user.failed_login_attempts += 1
            self.users[user.user_id] = user

            if user.failed_login_attempts >= self.config.max_failed_attempts:
                user.lock_account()
                self.users[user.user_id] = user
                raise AccountLockedError("Account locked due to too many failed attempts")

            raise InvalidCredentialsError("Invalid username or password")

        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        self.users[user.user_id] = user

        # Generate tokens
        tokens = self._generate_tokens(user)

        logger.info(f"User {username} authenticated successfully")
        return user, tokens

    def _generate_tokens(self, user: User) -> Dict[str, str]:
        """Generate access and refresh tokens"""
        # Generate access token
        access_token = self._create_token(
            user.user_id,
            user.username,
            user.role,
            expires_in=self.config.access_token_expiration
        )

        # Generate refresh token
        refresh_token = self._create_token(
            user.user_id,
            user.username,
            user.role,
            token_type="refresh",
            expires_in=self.config.refresh_token_expiration
        )

        # Store refresh token
        self.tokens[refresh_token] = {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "expires_at": datetime.utcnow() + timedelta(seconds=self.config.refresh_token_expiration)
        }

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": self.config.access_token_expiration
        }

    def _create_token(
        self,
        user_id: str,
        username: str,
        role: UserRole,
        token_type: str = "access",
        expires_in: int = None
    ) -> str:
        """Create a JWT token"""
        expires_in = expires_in or self.config.access_token_expiration
        payload = {
            "sub": user_id,
            "username": username,
            "role": role.name,
            "type": token_type,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=expires_in)
        }

        return jwt.encode(payload, self.config.jwt_secret, algorithm=self.config.jwt_algorithm)

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret,
                algorithms=[self.config.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthError("Invalid token")

    def refresh_tokens(self, refresh_token: str) -> Dict[str, str]:
        """Refresh access and refresh tokens"""
        # Verify refresh token
        try:
            payload = self.verify_token(refresh_token)

            # Check if it's a refresh token
            if payload.get("type") != "refresh":
                raise AuthError("Invalid token type")

            # Check if token is in storage
            if refresh_token not in self.tokens:
                raise AuthError("Invalid refresh token")

            # Get user and generate new tokens
            user_id = payload["sub"]
            user = self.users.get(user_id)

            if not user:
                raise AuthError("User not found")

            # Generate new tokens
            return self._generate_tokens(user)

        except TokenExpiredError:
            raise TokenExpiredError("Refresh token has expired")
        except AuthError:
            raise

    def authorize(self, user_id: str, required_permission: Permission):
        """Authorize a user for a specific permission"""
        user = self.users.get(user_id)

        if not user:
            raise AuthError("User not found")

        if user.is_locked():
            raise AccountLockedError("Account is locked")

        if not user.has_permission(required_permission):
            raise InsufficientPermissionsError("Insufficient permissions")

        return True

    def require_role(self, user_id: str, required_role: UserRole):
        """Require a specific role"""
        user = self.users.get(user_id)

        if not user:
            raise AuthError("User not found")

        if user.is_locked():
            raise AccountLockedError("Account is locked")

        if not user.role.has_permission(required_role):
            raise InsufficientPermissionsError("Insufficient role permissions")

        return True

    def enable_mfa(self, user_id: str, mfa_secret: str = None) -> str:
        """Enable multi-factor authentication for a user"""
        user = self.users.get(user_id)

        if not user:
            raise AuthError("User not found")

        # Generate MFA secret if not provided
        secret = mfa_secret or secrets.token_hex(16)
        user.mfa_enabled = True
        user.mfa_secret = secret
        self.users[user_id] = user

        return secret

    def disable_mfa(self, user_id: str):
        """Disable multi-factor authentication for a user"""
        user = self.users.get(user_id)

        if not user:
            raise AuthError("User not found")

        user.mfa_enabled = False
        user.mfa_secret = None
        self.users[user_id] = user

    def verify_mfa(self, user_id: str, code: str) -> bool:
        """Verify MFA code"""
        user = self.users.get(user_id)

        if not user or not user.mfa_enabled:
            raise AuthError("MFA not enabled for this user")

        # In a real implementation, this would use TOTP or similar
        # For this example, we'll just check if the code matches the secret
        return hmac.compare_digest(code, user.mfa_secret)

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        role: UserRole = UserRole.USER,
        permissions: List[Permission] = None
    ) -> User:
        """Create a new user"""
        # Validate password
        if not self._validate_password(password):
            raise ValueError("Password does not meet complexity requirements")

        # Check if user already exists
        for user in self.users.values():
            if user.username == username or user.email == email:
                raise ValueError("Username or email already exists")

        # Create user
        user = User(
            user_id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            role=role,
            status=UserStatus.ACTIVE,
            permissions=permissions or []
        )

        self.users[user.user_id] = user
        return user

    def update_user_password(self, user_id: str, new_password: str):
        """Update user password"""
        if not self._validate_password(new_password):
            raise ValueError("Password does not meet complexity requirements")

        user = self.users.get(user_id)

        if not user:
            raise AuthError("User not found")

        user.password_hash = self._hash_password(new_password)
        self.users[user_id] = user

    def unlock_user_account(self, user_id: str):
        """Unlock a user account"""
        user = self.users.get(user_id)

        if not user:
            raise AuthError("User not found")

        user.unlock_account()
        self.users[user_id] = user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID"""
        return self.users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

# Create a global authentication system instance
auth_system = EnhancedAuthSystem()

# Example usage
if __name__ == "__main__":
    print("Testing enhanced authentication system...")

    # Test authentication
    try:
        user, tokens = auth_system.authenticate("admin", "admin123")
        print(f"✓ Authentication successful: {user.username}")
        print(f"  Access token: {tokens['access_token'][:50]}...")
        print(f"  Refresh token: {tokens['refresh_token'][:50]}...")
    except AuthError as e:
        print(f"❌ Authentication failed: {e}")

    # Test token verification
    try:
        payload = auth_system.verify_token(tokens['access_token'])
        print(f"✓ Token verification successful: {payload}")
    except AuthError as e:
        print(f"❌ Token verification failed: {e}")

    # Test authorization
    try:
        auth_system.authorize(user.user_id, Permission.MANAGE_USERS)
        print(f"✓ Authorization successful for {Permission.MANAGE_USERS}")
    except AuthError as e:
        print(f"❌ Authorization failed: {e}")

    # Test role requirement
    try:
        auth_system.require_role(user.user_id, UserRole.ADMIN)
        print(f"✓ Role requirement successful for {UserRole.ADMIN}")
    except AuthError as e:
        print(f"❌ Role requirement failed: {e}")

    # Test MFA
    try:
        mfa_secret = auth_system.enable_mfa(user.user_id)
        print(f"✓ MFA enabled with secret: {mfa_secret}")

        mfa_verified = auth_system.verify_mfa(user.user_id, mfa_secret)
        print(f"✓ MFA verification: {mfa_verified}")
    except AuthError as e:
        print(f"❌ MFA failed: {e}")

    print("Enhanced authentication system test completed")





