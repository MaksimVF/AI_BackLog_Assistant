



#!/usr/bin/env python3

"""
Comprehensive test for admin functionality
"""

import os
import json
from fastapi.testclient import TestClient
from api.main import app
from security.jwt import create_access_token
from models.user import UserRole

def test_admin_functionality():
    """Test all admin functionality"""

    # Create test client
    client = TestClient(app)

    # Create admin token
    admin_token = create_access_token(
        data={
            "sub": "test_admin",
            "user_id": "test_admin_id",
            "role": UserRole.ADMIN
        }
    )

    print("=== Testing Admin Functionality ===\n")

    # Test 1: Admin Status
    print("1. Testing admin status...")
    response = client.get(
        "/admin/status",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")

    # Test 2: LLM Model Management
    print("2. Testing LLM model management...")

    # Get current models
    response = client.get(
        "/admin/llm/models",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Current models: {response.status_code}")
    if response.status_code == 200:
        print(f"   Models: {[m['name'] for m in response.json()['models']]}")

    # Create a new model
    new_model = {
        "name": "test-model",
        "provider": "local",
        "api_url": "http://localhost:5000/v1/models/test",
        "max_tokens": 2048,
        "temperature": 0.5,
        "is_default": False
    }

    response = client.post(
        "/admin/llm/models",
        json=new_model,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Create model: {response.status_code}")
    print(f"   Response: {response.json()}")

    # Set as default
    response = client.post(
        "/admin/llm/models/test-model/set_default",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Set default: {response.status_code}")
    print(f"   Response: {response.json()}")

    # Delete model
    response = client.delete(
        "/admin/llm/models/test-model",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Delete model: {response.status_code}")
    print(f"   Response: {response.json()}\n")

    # Test 3: Feature Management
    print("3. Testing feature management...")

    response = client.get(
        "/admin/features",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Features: {response.status_code}")
    if response.status_code == 200:
        features = response.json()['features']
        print(f"   Available features: {list(features.keys())}")

        # Test updating a feature (simulated)
        if 'CategorizationAgent' in features:
            response = client.post(
                "/admin/features/CategorizationAgent",
                json={"price": 1.5},
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            print(f"   Update feature: {response.status_code}")
            print(f"   Response: {response.json()}\n")

    # Test 4: Tariff Management (simulated - may fail due to DB context)
    print("4. Testing tariff management...")

    response = client.get(
        "/admin/tariffs",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Tariffs: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    else:
        print(f"   Response: {response.text}")

    # Test 5: Payment Management (simulated)
    print("\n5. Testing payment management...")

    response = client.get(
        "/admin/payments/history",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Payment history: {response.status_code}")
    if response.status_code == 200:
        print(f"   Transactions: {len(response.json()['transactions'])}")
    else:
        print(f"   Response: {response.text}")

    # Test manual transaction
    manual_tx = {
        "organization_id": "test-org-id",
        "amount": 1000.0,
        "description": "Test compensation"
    }

    response = client.post(
        "/admin/payments/manual",
        json=manual_tx,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"   Manual transaction: {response.status_code}")
    print(f"   Response: {response.json() if response.status_code == 200 else response.text}\n")

    print("=== Admin Functionality Test Completed ===")

if __name__ == "__main__":
    test_admin_functionality()


