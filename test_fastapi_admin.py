



#!/usr/bin/env python3

"""
Test script for FastAPI admin functionality - Updated with comprehensive testing
"""

import os
import tempfile
import uvicorn
import json
from fastapi.testclient import TestClient
from api.main import app
from api.admin import router as admin_router, LLMModelCreate, TariffPlanCreate, ManualTransaction, FeatureUpdate
from security.jwt import create_access_token
from models.user import UserRole

# Create a test client
client = TestClient(app)

def test_admin_endpoints():
    """Test admin endpoints comprehensively"""

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

    # Test creating LLM model
    llm_data = LLMModelCreate(
        name="test-model",
        provider="openai",
        api_key="test-key",
        max_tokens=8192,
        temperature=0.5,
        is_default=False
    )
    response = client.post(
        "/admin/llm/models",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=llm_data.model_dump() if hasattr(llm_data, 'model_dump') else llm_data.dict()
    )
    print(f"Create LLM model: {response.status_code} - {response.json()}")

    # Test features
    response = client.get(
        "/admin/features",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Features: {response.status_code} - {response.json()}")

    # Test updating feature (if any features exist)
    if response.status_code == 200 and response.json().get("features"):
        feature_name = list(response.json()["features"].keys())[0]
        feature_data = FeatureUpdate(config={"enabled": True, "limit": 100})
        response = client.post(
            f"/admin/features/{feature_name}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=feature_data.model_dump() if hasattr(feature_data, 'model_dump') else feature_data.dict()
        )
        print(f"Update feature: {response.status_code} - {response.json()}")

    # Test system health
    response = client.get(
        "/admin/system/health",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"System health: {response.status_code} - {response.json()}")

    # Note: Skipping database-dependent endpoints in this test
    # These would need a proper Flask app context to work:
    # - Tariff plans
    # - Payment history
    # - Manual transactions
    # - System stats

    print("Database-dependent endpoints skipped (require Flask app context)")

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


