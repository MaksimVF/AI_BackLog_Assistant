


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from security.jwt import verify_token, TokenData
from models.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Get the current user from the JWT token"""
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def require_role(role: UserRole):
    """Create a dependency that requires a specific user role"""
    def role_checker(user: TokenData = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user
    return role_checker

