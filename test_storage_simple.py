#!/usr/bin/env python3

"""
Simple test script to verify storage integration with tariff plans
"""

import sqlite3
import os
import uuid
from datetime import datetime

def test_storage_integration():
    """Test that storage fields are properly integrated with tariff plans."""
    db_path = 'instance/site.db'

    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if storage columns exist
    cursor.execute("PRAGMA table_info(tariff_plans)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]

    print("Table columns:", column_names)

    expected_columns = [
        'included_storage_gb',
        'additional_storage_price_per_gb',
        'storage_retention_days',
        'storage_tier'
    ]

    missing_columns = []
    for col in expected_columns:
        if col not in column_names:
            missing_columns.append(col)

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
    else:
        print("All storage columns are present in tariff_plans table")

    # Test inserting a tariff plan with storage fields
    try:
        plan_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO tariff_plans
            (id, name, price_per_month, included_limits, discounts, access_features,
             created_at, updated_at,
             included_storage_gb, additional_storage_price_per_gb, storage_retention_days, storage_tier)
            VALUES
            (?, 'Test Plan', 1000.0, '{}', '{}', 'feature1,feature2',
             ?, ?,
             10.0, 5.0, 365, 'premium')
        """, (plan_id, now, now))
        conn.commit()
        print("Successfully inserted test tariff plan with storage fields")

        # Verify the insertion
        cursor.execute("SELECT * FROM tariff_plans WHERE name = 'Test Plan'")
        plan = cursor.fetchone()
        if plan:
            plan_dict = dict(zip(column_names, plan))
            print(f"Retrieved plan: {plan_dict}")
            # Check storage fields specifically
            print(f"Storage fields: included_storage_gb={plan_dict['included_storage_gb']}, "
                  f"additional_storage_price_per_gb={plan_dict['additional_storage_price_per_gb']}, "
                  f"storage_retention_days={plan_dict['storage_retention_days']}, "
                  f"storage_tier={plan_dict['storage_tier']}")
        else:
            print("Failed to retrieve the inserted plan")

    except Exception as e:
        print(f"Error inserting test plan: {e}")
        conn.rollback()

    conn.close()
    print("Storage integration test completed")

if __name__ == "__main__":
    test_storage_integration()
