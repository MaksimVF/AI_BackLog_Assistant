


#!/usr/bin/env python3

"""
Simple Database Migration Script for Storage Pricing
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspace/AI_BackLog_Assistant/instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class StoragePricing(db.Model):
    """Storage pricing configuration"""
    __tablename__ = 'storage_pricing'

    tier = db.Column(db.String(20), primary_key=True)  # free, standard, premium, custom
    price_per_gb_month = db.Column(db.Float, nullable=False, default=0.0)
    retention_days = db.Column(db.Integer, nullable=False, default=180)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'tier': self.tier,
            'price_per_gb_month': self.price_per_gb_month,
            'retention_days': self.retention_days,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

def migrate():
    """Migrate the database to add storage pricing table."""
    with app.app_context():
        # Create storage_pricing table
        try:
            db.create_all()  # This will create the storage_pricing table
            print("Storage pricing table created successfully")

            # Add default pricing tiers if they don't exist
            if not StoragePricing.query.filter_by(tier='free').first():
                free_tier = StoragePricing(
                    tier='free',
                    price_per_gb_month=0.0,
                    retention_days=30,
                    description='Free tier with limited storage'
                )
                db.session.add(free_tier)

            if not StoragePricing.query.filter_by(tier='standard').first():
                standard_tier = StoragePricing(
                    tier='standard',
                    price_per_gb_month=10.0,
                    retention_days=180,
                    description='Standard storage tier'
                )
                db.session.add(standard_tier)

            if not StoragePricing.query.filter_by(tier='premium').first():
                premium_tier = StoragePricing(
                    tier='premium',
                    price_per_gb_month=20.0,
                    retention_days=365,
                    description='Premium storage tier'
                )
                db.session.add(premium_tier)

            db.session.commit()
            print("Default storage pricing tiers added")

        except Exception as e:
            db.session.rollback()
            print(f"Error creating storage pricing table: {e}")

        print("Storage database migration completed")

if __name__ == "__main__":
    migrate()


