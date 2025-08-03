















#!/usr/bin/env python3

"""
Database Migration Script for Billing System Updates
"""

from web_server.app import app, db
from web_server.billing_models import TariffPlan, OrganizationBalance
from sqlalchemy.sql import text

def migrate_database():
    """Migrate the database to include new fields."""
    with app.app_context():
        # Add new columns to existing tables
        try:
            # Add team_members to OrganizationBalance
            db.session.execute(text("""
                ALTER TABLE organization_balances
                ADD COLUMN team_members INTEGER DEFAULT 1
            """))
            print("Added team_members column to organization_balances")
        except Exception as e:
            print(f"Error adding team_members column: {e}")

        try:
            # Add max_team_members and member_price to TariffPlan
            db.session.execute(text("""
                ALTER TABLE tariff_plans
                ADD COLUMN max_team_members INTEGER DEFAULT 1
            """))
            db.session.execute(text("""
                ALTER TABLE tariff_plans
                ADD COLUMN member_price FLOAT DEFAULT 0.0
            """))
            print("Added max_team_members and member_price columns to tariff_plans")
        except Exception as e:
            print(f"Error adding tariff columns: {e}")

        db.session.commit()
        print("Database migration completed")

if __name__ == "__main__":
    migrate_database()















