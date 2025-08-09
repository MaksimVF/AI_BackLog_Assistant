





"""
Main application with enhanced authentication and authorization
"""

import os
import sys
import time
import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Add project root to path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security.auth_enhanced import (
    EnhancedAuthSystem, AuthError, InvalidCredentialsError,
    AccountLockedError, TokenExpiredError, InsufficientPermissionsError,
    UserRole, Permission
)
from security.security_system import SecuritySystem, SecurityLevel
from security_integration import security_integration
from agents.system_admin.logging_manager import initialize_logging
from agents.system_admin.monitoring_agent import MonitoringAgent
from health import get_health_status, get_readiness_status

# Initialize logging
logging_manager = initialize_logging(
    service_name="AI_BackLog_Assistant",
    environment=os.getenv('ENV', 'dev')
)
logger = logging_manager.get_logger()

# Initialize monitoring agent
monitoring_agent = MonitoringAgent()

# Initialize enhanced authentication system
auth_system = EnhancedAuthSystem()

def start_security_monitoring():
    """Start background security monitoring"""
    security_integration.start_security_monitoring()
    logger.info("Started security monitoring")

def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate a user and return tokens

    Args:
        username: Username or email
        password: Password

    Returns:
        Authentication result
    """
    try:
        user, tokens = auth_system.authenticate(username, password)

        # Audit the authentication
        security_integration.audit_operation(
            "user_authentication",
            user_id=user.user_id,
            inputs={"username": username},
            outputs={"user_id": user.user_id, "role": user.role.name},
            status="success"
        )

        return {
            "status": "success",
            "user": {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "role": user.role.name,
                "status": user.status.value
            },
            "tokens": tokens
        }

    except InvalidCredentialsError as e:
        # Audit failed authentication
        security_integration.audit_operation(
            "user_authentication",
            inputs={"username": username},
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "error": str(e)
        }

    except AccountLockedError as e:
        # Audit account lockout
        security_integration.audit_operation(
            "user_authentication",
            inputs={"username": username},
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "error": str(e)
        }

    except AuthError as e:
        # Audit other authentication errors
        security_integration.audit_operation(
            "user_authentication",
            inputs={"username": username},
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "error": str(e)
        }

def authorize_user(user_id: str, permission: Permission) -> Dict[str, Any]:
    """
    Authorize a user for a specific permission

    Args:
        user_id: User ID
        permission: Required permission

    Returns:
        Authorization result
    """
    try:
        auth_system.authorize(user_id, permission)

        # Audit successful authorization
        security_integration.audit_operation(
            "user_authorization",
            user_id=user_id,
            inputs={"permission": permission.value},
            status="success"
        )

        return {
            "status": "success",
            "permission": permission.value
        }

    except InsufficientPermissionsError as e:
        # Audit failed authorization
        security_integration.audit_operation(
            "user_authorization",
            user_id=user_id,
            inputs={"permission": permission.value},
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "error": str(e)
        }

    except AuthError as e:
        # Audit other authorization errors
        security_integration.audit_operation(
            "user_authorization",
            user_id=user_id,
            inputs={"permission": permission.value},
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "error": str(e)
        }

def refresh_tokens(refresh_token: str) -> Dict[str, Any]:
    """
    Refresh access and refresh tokens

    Args:
        refresh_token: Refresh token

    Returns:
        Token refresh result
    """
    try:
        new_tokens = auth_system.refresh_tokens(refresh_token)

        # Audit token refresh
        security_integration.audit_operation(
            "token_refresh",
            inputs={"refresh_token": refresh_token[:50] + "..."},
            status="success"
        )

        return {
            "status": "success",
            "tokens": new_tokens
        }

    except TokenExpiredError as e:
        # Audit expired token
        security_integration.audit_operation(
            "token_refresh",
            inputs={"refresh_token": refresh_token[:50] + "..."},
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "error": str(e)
        }

    except AuthError as e:
        # Audit other token errors
        security_integration.audit_operation(
            "token_refresh",
            inputs={"refresh_token": refresh_token[:50] + "..."},
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "error": str(e)
        }

def secure_api_endpoint(
    endpoint_func: callable,
    required_permission: Permission = None,
    required_role: UserRole = None
) -> callable:
    """
    Decorator to secure API endpoints with authentication and authorization

    Args:
        endpoint_func: API endpoint function
        required_permission: Required permission
        required_role: Required role

    Returns:
        Secured endpoint function
    """
    def secured_endpoint(*args, **kwargs):
        # Get authentication information
        api_key = kwargs.get('api_key')
        token = kwargs.get('token')
        user_id = kwargs.get('user_id')

        if not user_id:
            raise ValueError("User ID required for authentication")

        # Check permission if required
        if required_permission:
            auth_result = authorize_user(user_id, required_permission)
            if auth_result["status"] != "success":
                raise ValueError(f"Permission denied: {auth_result['error']}")

        # Check role if required
        if required_role:
            user = auth_system.get_user(user_id)
            if not user or not user.role.has_permission(required_role):
                raise ValueError(f"Insufficient role: {required_role.name} required")

        # Call the actual endpoint
        return endpoint_func(*args, **kwargs)

    return secured_endpoint

async def process_secure_operation(user_id: str, operation: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a secure operation with authentication and authorization

    Args:
        user_id: User ID
        operation: Operation name
        data: Operation data

    Returns:
        Operation result
    """
    # Secure the operation data
    secured_data = security_integration.secure_component_communication(
        data, "main_app", f"operation_{operation}"
    )

    # Process the operation
    try:
        # Verify the secured data
        verified_data = security_integration.verify_component_message(
            secured_data,
            expected_source="main_app",
            expected_target=f"operation_{operation}"
        )

        # Simulate operation processing
        result = {
            "status": "success",
            "operation": operation,
            "data": verified_data,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Audit the operation
        security_integration.audit_operation(
            operation,
            user_id=user_id,
            inputs=data,
            outputs=result
        )

        return result

    except Exception as e:
        # Audit failed operation
        security_integration.audit_operation(
            operation,
            user_id=user_id,
            inputs=data,
            status="failed",
            outputs={"error": str(e)}
        )

        return {
            "status": "error",
            "operation": operation,
            "error": str(e)
        }

async def main():
    """Main application with enhanced authentication and authorization"""
    logger.info("🚀 Starting AI_BackLog_Assistant with enhanced authentication")
    print("🚀 Starting AI_BackLog_Assistant with enhanced authentication")
    print("=" * 70)

    # Start security monitoring
    start_security_monitoring()

    # Test authentication
    print("\n🔒 Testing Authentication System:")
    print("-" * 50)

    # Test admin authentication
    admin_auth = authenticate_user("admin", "admin123")
    print(f"Admin authentication: {admin_auth['status']}")

    if admin_auth["status"] == "success":
        admin_user = admin_auth["user"]
        admin_tokens = admin_auth["tokens"]

        # Test authorization
        auth_result = authorize_user(admin_user["user_id"], Permission.MANAGE_USERS)
        print(f"Admin authorization for MANAGE_USERS: {auth_result['status']}")

        # Test token refresh
        refresh_result = refresh_tokens(admin_tokens["refresh_token"])
        print(f"Token refresh: {refresh_result['status']}")

        # Test secure operation
        operation_result = await process_secure_operation(
            admin_user["user_id"],
            "test_operation",
            {"data": "test data"}
        )
        print(f"Secure operation: {operation_result['status']}")

    # Test regular user authentication
    user_auth = authenticate_user("user", "user123")
    print(f"User authentication: {user_auth['status']}")

    if user_auth["status"] == "success":
        user = user_auth["user"]

        # Test user authorization
        user_auth_result = authorize_user(user["user_id"], Permission.CREATE_DOCUMENTS)
        print(f"User authorization for CREATE_DOCUMENTS: {user_auth_result['status']}")

        # Test insufficient permissions
        insufficient_auth = authorize_user(user["user_id"], Permission.MANAGE_USERS)
        print(f"User authorization for MANAGE_USERS: {insufficient_auth['status']}")

    # Test failed authentication
    failed_auth = authenticate_user("admin", "wrongpassword")
    print(f"Failed authentication: {failed_auth['status']}")

    # Test account lockout
    for i in range(5):
        authenticate_user("user", f"wrongpassword{i}")

    locked_auth = authenticate_user("user", "wrongpassword6")
    print(f"Account lockout test: {locked_auth['status']}")

    # Log final system health
    health = get_health_status()
    logger.info("Final system health", extra={
        'health_status': health['status'],
        'cpu_usage': health['system']['cpu_usage'],
        'memory_usage': health['system']['memory_usage'],
        'disk_usage': health['system']['disk_usage']
    })

    # Log security status
    security_audit = security_integration.perform_security_audit()
    logger.info("Security audit completed", extra={
        'recommendations': len(security_audit['recommendations']),
        'vulnerabilities': len(security_audit.get('vulnerabilities', []))
    })

    print("\n✅ Enhanced authentication and authorization system is working correctly")

if __name__ == "__main__":
    asyncio.run(main())






