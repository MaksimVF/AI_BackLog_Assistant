



"""
Extensions initialization for AI Backlog Assistant
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from argon2 import PasswordHasher

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
ph = PasswordHasher()


