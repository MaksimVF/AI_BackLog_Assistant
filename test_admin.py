


#!/usr/bin/env python3

"""
Test script for admin functionality
"""

import os
import tempfile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from web_server.models import User
from web_server.extensions import db
from web_server.admin_simple import admin_bp

# Create a test Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprint
app.register_blueprint(admin_bp)

# Create database and tables
with app.app_context():
    db.create_all()

    # Create a test admin user if doesn't exist
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin_user.set_password('admin123')

        db.session.add(admin_user)
        db.session.commit()
        print("Test admin user created:")
    else:
        print("Test admin user already exists:")

    print(f"Username: admin")
    print(f"Password: admin123")
    print(f"Role: {admin_user.role}")

if __name__ == '__main__':
    app.run(debug=True, port=52551)

