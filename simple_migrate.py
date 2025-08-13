


#!/usr/bin/env python3

"""
Simple Database Migration Script for Storage Fields
"""

import sqlite3
import os

def migrate_database():
    """Migrate the database to include new storage fields."""
    db_path = 'instance/site.db'

    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Add storage-related columns to tariff_plans
        cursor.execute("""
            ALTER TABLE tariff_plans
            ADD COLUMN included_storage_gb FLOAT DEFAULT 0.0
        """)
        print("Added included_storage_gb column to tariff_plans")
    except sqlite3.OperationalError as e:
        if 'duplicate column' in str(e).lower():
            print("included_storage_gb column already exists")
        else:
            print(f"Error adding included_storage_gb column: {e}")

    try:
        cursor.execute("""
            ALTER TABLE tariff_plans
            ADD COLUMN additional_storage_price_per_gb FLOAT DEFAULT 0.0
        """)
        print("Added additional_storage_price_per_gb column to tariff_plans")
    except sqlite3.OperationalError as e:
        if 'duplicate column' in str(e).lower():
            print("additional_storage_price_per_gb column already exists")
        else:
            print(f"Error adding additional_storage_price_per_gb column: {e}")

    try:
        cursor.execute("""
            ALTER TABLE tariff_plans
            ADD COLUMN storage_retention_days INTEGER DEFAULT 180
        """)
        print("Added storage_retention_days column to tariff_plans")
    except sqlite3.OperationalError as e:
        if 'duplicate column' in str(e).lower():
            print("storage_retention_days column already exists")
        else:
            print(f"Error adding storage_retention_days column: {e}")

    try:
        cursor.execute("""
            ALTER TABLE tariff_plans
            ADD COLUMN storage_tier VARCHAR(20) DEFAULT 'standard'
        """)
        print("Added storage_tier column to tariff_plans")
    except sqlite3.OperationalError as e:
        if 'duplicate column' in str(e).lower():
            print("storage_tier column already exists")
        else:
            print(f"Error adding storage_tier column: {e}")

    conn.commit()
    conn.close()
    print("Database migration completed")

if __name__ == "__main__":
    migrate_database()


