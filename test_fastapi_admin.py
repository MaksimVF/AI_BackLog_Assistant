



#!/usr/bin/env python3

"""
Test script for FastAPI admin functionality
"""

import os
import tempfile
import uvicorn
from fastapi.testclient import TestClient
from api.main import app
from api.admin import router as admin_router
from security.jwt import create_access_token
from models.user import UserRole

# Create a test client
client = TestClient(app)

def test_admin_endpoints():
    """Test admin endpoints"""

    # Create a test admin token
    admin_token = create_access_token(
        data={
            "sub": "test_admin",
            "user_id": "test_admin_id",
            "role": UserRole.ADMIN
        }
    )

    print("Testing admin endpoints...")

    # Test admin status
    response = client.get(
        "/admin/status",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Admin status: {response.status_code} - {response.json()}")

    # Test LLM models
    response = client.get(
        "/admin/llm/models",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"LLM models: {response.status_code} - {response.json()}")

    # Test tariff plans
    response = client.get(
        "/admin/tariffs",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Tariff plans: {response.status_code} - {response.json()}")

    # Test features
    response = client.get(
        "/admin/features",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Features: {response.status_code} - {response.json()}")

    # Test payment history
    response = client.get(
        "/admin/payments/history",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Payment history: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_admin_endpoints()
    print("Admin endpoint testing completed!")

    # Also run the FastAPI server for manual testing
    print("\nStarting FastAPI server on http://localhost:8000")
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


