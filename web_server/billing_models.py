
"""
Billing System Models for AI Backlog Assistant
"""

import uuid
import datetime
from datetime import datetime
from typing import Dict, Any, Optional
from .app import db

class TariffPlan(db.Model):
    """Model for tariff plans with included limits and discounts."""
    __tablename__ = 'tariff_plans'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False, unique=True)  # Free, Pro, Team, etc.
    price_per_month = db.Column(db.Float, nullable=False, default=0.0)
    included_limits = db.Column(db.JSON, nullable=False, default=dict)  # {"feature_name": limit}
    discounts = db.Column(db.JSON, nullable=False, default=dict)  # {"PAYG": discount_rate}
    access_features = db.Column(db.JSON, nullable=False, default=list)  # Premium/exclusive features
    max_team_members = db.Column(db.Integer, default=1)  # Максимум членов команды
    member_price = db.Column(db.Float, default=0.0)  # Цена за дополнительного члена
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"TariffPlan('{self.name}', '{self.price_per_month}')"

class OrganizationBalance(db.Model):
    """Model for tracking organization balances."""
    __tablename__ = 'organization_balances'

    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), primary_key=True)
    balance_rub = db.Column(db.Float, nullable=False, default=0.0)
    auto_recharge = db.Column(db.Boolean, nullable=False, default=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    tariff_plan_id = db.Column(db.String(36), db.ForeignKey('tariff_plans.id'), nullable=True)
    team_members = db.Column(db.Integer, default=1)  # Количество членов команды

    # Relationship to Organization and TariffPlan
    organization = db.relationship('Organization', backref=db.backref('balance', lazy=True, uselist=False))
    tariff_plan = db.relationship('TariffPlan', backref=db.backref('organizations', lazy=True))

    def __repr__(self):
        return f"OrganizationBalance('{self.organization_id}', '{self.balance_rub}')"

class UsageLog(db.Model):
    """Model for logging feature usage and billing events."""
    __tablename__ = 'usage_logs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    feature = db.Column(db.String(100), nullable=False)  # Feature name (e.g., "CategorizationAgent")
    units_used = db.Column(db.Integer, nullable=False, default=1)  # Number of units used
    tokens_used = db.Column(db.Integer, nullable=True)  # Optional: tokens used
    price_charged = db.Column(db.Float, nullable=False, default=0.0)  # Amount charged
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    additional_data = db.Column(db.JSON, nullable=True)  # Additional context

    # Relationships
    organization = db.relationship('Organization')
    user = db.relationship('User')

    def __repr__(self):
        return f"UsageLog('{self.feature}', '{self.units_used}', '{self.price_charged}')"

class FeatureConfig(db.Model):
    """Model for feature configuration (pricing, access, etc.)."""
    __tablename__ = 'feature_configs'

    feature_name = db.Column(db.String(100), primary_key=True)
    feature_type = db.Column(db.String(20), nullable=False)  # basic, premium, exclusive
    unit = db.Column(db.String(20), nullable=False)  # call, token, etc.
    price_per_unit = db.Column(db.Float, nullable=False)
    access_tariffs = db.Column(db.JSON, nullable=True)  # Tariffs that can access
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"FeatureConfig('{self.feature_name}', '{self.price_per_unit}')"
