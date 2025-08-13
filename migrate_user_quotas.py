


#!/usr/bin/env python3

"""
Database Migration Script for User Storage Quotas
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text

# Create a minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspace/AI_BackLog_Assistant/instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def migrate_user_quotas():
    """Migrate the database to add storage quota fields to users table."""
    with app.app_context():
        try:
            # Add storage quota fields to users table
            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN storage_quota_mb INTEGER DEFAULT 5120
            """))
            print("Added storage_quota_mb column to users")

            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN storage_retention_days INTEGER DEFAULT 180
            """))
            print("Added storage_retention_days column to users")

            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN storage_tier VARCHAR(20) DEFAULT 'free'
            """))
            print("Added storage_tier column to users")

            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN storage_expiration DATETIME
            """))
            print("Added storage_expiration column to users")

            db.session.commit()
            print("User storage quota migration completed successfully")

        except Exception as e:
            db.session.rollback()
            print(f"Error during user storage quota migration: {e}")

if __name__ == "__main__":
    migrate_user_quotas()


