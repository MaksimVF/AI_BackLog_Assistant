




"""
API Security Middleware and Utilities
"""

import os
import time
import hmac
import hashlib
import logging
from typing import Any, Callable, Dict, List, Optional, Union
from fastapi import Request, Response, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from utils.error_handling import SecurityError
from utils.validation import InputValidator, validate_pydantic_model
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class APISecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for API security checks"""

    def __init__(
        self,
        app: ASGIApp,
        exclude_paths: Optional[list] = None,
        rate_limit: Optional[int] = None
    ):
        super().__init__(app)
        self.exclude_paths = exclude_paths or []
        self.rate_limit = rate_limit
        self.request_counts: Dict[str, int] = {}
        self.request_timestamps: Dict[str, float] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process incoming requests with security checks"""
        path = request.url.path

        # Skip security checks for excluded paths
        if any(path.startswith(excluded) for excluded in self.exclude_paths):
            return await call_next(request)

        # Rate limiting
        if self.rate_limit:
            client_ip = self._get_client_ip(request)
            current_time = time.time()

            # Reset count if time window has passed (simple implementation)
            if (client_ip in self.request_timestamps and
                current_time - self.request_timestamps[client_ip] > 60):
                self.request_counts[client_ip] = 0

            # Check rate limit
            if client_ip in self.request_counts and self.request_counts[client_ip] >= self.rate_limit:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests",
                    headers={"Retry-After": "60"}
                )

            # Increment count
            self.request_counts[client_ip] = self.request_counts.get(client_ip, 0) + 1
            self.request_timestamps[client_ip] = current_time

        # Input validation for common endpoints
        if path.startswith("/api/process"):
            try:
                await self._validate_process_request(request)
            except SecurityError as e:
                raise HTTPException(status_code=400, detail=str(e))

        # Continue to next middleware/endpoint
        return await call_next(request)

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            # Take the first IP in the list
            return forwarded_for.split(',')[0].strip()
        return request.client.host

    async def _validate_process_request(self, request: Request) -> None:
        """Validate document processing requests"""
        try:
            # Parse request body
            body = await request.json()
            expected_fields = ['document_id', 'content']

            # Validate and sanitize
            validated_data = InputValidator.validate_and_sanitize_request(body, expected_fields)

            # Update request with validated data
            request.state.validated_data = validated_data

        except Exception as e:
            logger.warning(f"Request validation failed: {str(e)}")
            raise SecurityError(f"Invalid request: {str(e)}")

class JWTBearer(HTTPBearer):
    """JWT Authentication for FastAPI"""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        """Extract and validate JWT token"""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme"
                )

            if not self._verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token"
                )

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code"
            )

    def _verify_jwt(self, jwt_token: str) -> bool:
        """Verify JWT token signature and expiration"""
        try:
            payload = self._decode_jwt(jwt_token)
            return True
        except (JWTError, Exception):
            return False

    def _decode_jwt(self, jwt_token: str) -> Dict[str, Any]:
        """Decode JWT token and return payload"""
        try:
            return jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as e:
            raise SecurityError(f"JWT decoding failed: {str(e)}")

def create_jwt_token(
    data: Dict[str, Any],
    expires_delta: Optional[int] = None
) -> str:
    """
    Create a JWT token with optional expiration

    Args:
        data: Data to encode in the token
        expires_delta: Expiration time in minutes (None for no expiration)

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = time.time() + expires_delta * 60
        to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload

    Raises:
        SecurityError: If token is invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise SecurityError(f"JWT verification failed: {str(e)}")

def generate_hmac_signature(data: str, secret: str = SECRET_KEY) -> str:
    """
    Generate HMAC signature for data integrity

    Args:
        data: Data to sign
        secret: Secret key for HMAC

    Returns:
        HMAC signature (hex encoded)
    """
    return hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()

def verify_hmac_signature(data: str, signature: str, secret: str = SECRET_KEY) -> bool:
    """
    Verify HMAC signature

    Args:
        data: Original data
        signature: Signature to verify
        secret: Secret key for HMAC

    Returns:
        True if signature is valid, False otherwise
    """
    expected_signature = generate_hmac_signature(data, secret)
    return hmac.compare_digest(expected_signature, signature)

def secure_endpoint(
    endpoint_func: Callable,
    required_permissions: Optional[list] = None
) -> Callable:
    """
    Decorator to secure FastAPI endpoints

    Args:
        endpoint_func: Endpoint function to secure
        required_permissions: List of required permissions

    Returns:
        Secured endpoint function
    """
    async def wrapper(*args, **kwargs):
        # Extract request from args
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break

        if not request:
            raise HTTPException(status_code=400, detail="Invalid request")

        # Check authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = auth_header.split(' ')[1]

        try:
            # Verify JWT token
            payload = verify_jwt_token(token)

            # Check permissions if required
            if required_permissions:
                user_permissions = payload.get('permissions', [])
                missing_permissions = [
                    perm for perm in required_permissions
                    if perm not in user_permissions
                ]
                if missing_permissions:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Missing permissions: {', '.join(missing_permissions)}"
                    )

            # Add user info to request state
            request.state.user = payload

        except SecurityError as e:
            raise HTTPException(status_code=401, detail=str(e))

        # Call the original endpoint
        return await endpoint_func(*args, **kwargs)

    return wrapper

def validate_api_request(
    request_data: Dict[str, Any],
    model_class: type(BaseModel)
) -> Dict[str, Any]:
    """
    Validate API request against a Pydantic model

    Args:
        request_data: Raw request data
        model_class: Pydantic model to validate against

    Returns:
        Validated and sanitized data

    Raises:
        HTTPException: If validation fails
    """
    try:
        return validate_pydantic_model(model_class, request_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

def sanitize_api_input(data: Union[Dict[str, Any], List[Any]]) -> Union[Dict[str, Any], List[Any]]:
    """
    Sanitize API input to prevent injection attacks

    Args:
        data: Input data to sanitize

    Returns:
        Sanitized data
    """
    from utils.validation import InputValidator

    if isinstance(data, dict):
        return InputValidator.validate_and_sanitize_request(data, [])
    elif isinstance(data, list):
        return [sanitize_api_input(item) for item in data]
    else:
        return data

def check_content_security_policy(
    request: Request,
    allowed_sources: Optional[list] = None
) -> None:
    """
    Check Content Security Policy for API requests

    Args:
        request: FastAPI request object
        allowed_sources: List of allowed origin patterns

    Raises:
        HTTPException: If request violates CSP
    """
    origin = request.headers.get('Origin', '')
    referer = request.headers.get('Referer', '')

    if allowed_sources:
        allowed = False
        for pattern in allowed_sources:
            if (origin and pattern in origin) or (referer and pattern in referer):
                allowed = True
                break

        if not allowed:
            raise HTTPException(
                status_code=403,
                detail="Request violates Content Security Policy"
            )

def generate_secure_response(
    response_data: Dict[str, Any],
    include_signature: bool = False
) -> Dict[str, Any]:
    """
    Generate a secure API response with optional signature

    Args:
        response_data: Data to include in response
        include_signature: Whether to include HMAC signature

    Returns:
        Secure response with signature if requested
    """
    secure_response = {
        'status': 'success',
        'data': response_data,
        'timestamp': int(time.time())
    }

    if include_signature:
        # Generate signature of the data (excluding the signature field itself)
        data_str = str(response_data)
        secure_response['signature'] = generate_hmac_signature(data_str)

    return secure_response

class APIRateLimiter:
    """Rate limiter for API endpoints"""

    def __init__(self, limit: int = 100, window: int = 60):
        """
        Initialize rate limiter

        Args:
            limit: Maximum requests per window
            window: Time window in seconds
        """
        self.limit = limit
        self.window = window
        self.requests: Dict[str, List[float]] = {}

    def check_limit(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limit"""
        current_time = time.time()

        # Remove old requests outside the window
        if client_ip in self.requests:
            self.requests[client_ip] = [
                timestamp for timestamp in self.requests[client_ip]
                if current_time - timestamp < self.window
            ]

        # Check limit
        if client_ip in self.requests and len(self.requests[client_ip]) >= self.limit:
            return False

        # Record new request
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(current_time)

        return True

    def get_retry_after(self, client_ip: str) -> int:
        """Get time until rate limit resets"""
        if client_ip not in self.requests or not self.requests[client_ip]:
            return 0

        oldest_request = min(self.requests[client_ip])
        current_time = time.time()
        elapsed = current_time - oldest_request
        remaining = max(0, int(self.window - elapsed))

        return remaining

def create_api_security_middleware(
    app: ASGIApp,
    exclude_paths: Optional[list] = None,
    rate_limit: Optional[int] = None
) -> APISecurityMiddleware:
    """
    Create API security middleware instance

    Args:
        app: FastAPI app instance
        exclude_paths: Paths to exclude from security checks
        rate_limit: Requests per minute limit

    Returns:
        Configured middleware
    """
    return APISecurityMiddleware(
        app=app,
        exclude_paths=exclude_paths or ['/health', '/docs', '/openapi.json'],
        rate_limit=rate_limit
    )





