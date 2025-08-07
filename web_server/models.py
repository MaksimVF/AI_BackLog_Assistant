




"""
Database Models for AI Backlog Assistant
"""

import os
import uuid
import datetime
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from argon2.exceptions import VerifyMismatchError

# Initialize database
from .extensions import db, ph

# Association table for many-to-many relationship between users and organizations
class OrganizationMember(db.Model):
    __tablename__ = 'organization_members'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')  # owner, admin, member, viewer
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define relationship to User and Organization
    user = db.relationship('User', backref=db.backref('organization_memberships', lazy=True))
    organization = db.relationship('Organization', backref=db.backref('members', lazy=True))

    def __repr__(self):
        return f"OrganizationMember('{self.user_id}', '{self.organization_id}', '{self.role}')"

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=True)  # Nullable for OAuth users

    telegram_id = db.Column(db.String(64), unique=True, nullable=True)
    github_id = db.Column(db.String(64), unique=True, nullable=True)
    gitlab_id = db.Column(db.String(64), unique=True, nullable=True)
    bitbucket_id = db.Column(db.String(64), unique=True, nullable=True)
    google_id = db.Column(db.String(64), unique=True, nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    role = db.Column(db.String(20), nullable=False, default='user')  # user, admin
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        """Hash password using argon2"""
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        """Verify password using argon2"""
        try:
            return ph.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Organization model
class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship to the user who created the organization
    creator = db.relationship('User', backref=db.backref('created_organizations', lazy=True))

    def __repr__(self):
        return f"Organization('{self.name}')"

# Active context model (for tracking user's current organization context)
class ActiveContext(db.Model):
    __tablename__ = 'active_contexts'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    current_organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True)

    # Relationship to User and Organization
    user = db.relationship('User', backref=db.backref('active_context', lazy=True, uselist=False))
    organization = db.relationship('Organization')

# Document model for storing uploaded and processed documents
class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='uploaded')  # uploaded, processing, processed, analyzed
    extracted_text = db.Column(db.Text, nullable=True)
    file_metadata = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('documents', lazy=True))
    organization = db.relationship('Organization', backref=db.backref('documents', lazy=True))
    analyses = db.relationship('DocumentAnalysis', backref='document', lazy=True)

    def __repr__(self):
        return f"Document('{self.filename}', '{self.status}')"

# Document analysis model for storing analysis results
class DocumentAnalysis(db.Model):
    __tablename__ = 'document_analyses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey('documents.id'), nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False)  # basic, sentiment, entity, etc.
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, processing, completed, failed
    results = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"DocumentAnalysis('{self.analysis_type}', '{self.status}')"




