


from models.user import User, UserCreate, UserRole
from typing import Dict, Optional
import bcrypt

class UserDatabase:
    """Simple in-memory user database for demonstration purposes"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        # Create a default admin user
        self.create_user(UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123",
            role=UserRole.ADMIN
        ))

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user"""
        user = User(
            username=user_create.username,
            email=user_create.email,
            role=user_create.role
        )
        user.set_password(user_create.password)
        self.users[user.username] = user
        return user

    def get_user(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.users.get(username)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = self.get_user(username)
        if user and user.check_password(password):
            return user
        return None

# Global user database instance
user_db = UserDatabase()

