



"""
Security Demo for AI Backlog Assistant

This script demonstrates the security features implemented in the project.
"""

import requests
import json
import getpass

def main():
    base_url = "http://localhost:8000"

    print("🔒 AI Backlog Assistant - Security Demo")
    print("=" * 50)

    # Test 1: Register a new user
    print("\n1. Registering a new user...")

    username = input("Enter username: ") or "testuser"
    email = input("Enter email: ") or "test@example.com"
    password = getpass.getpass("Enter password: ") or "testpassword"

    register_data = {
        "username": username,
        "email": email,
        "password": password,
        "role": "user"
    }

    response = requests.post(
        f"{base_url}/auth/register",
        json=register_data
    )

    if response.status_code == 200:
        print("✅ User registered successfully!")
    else:
        print(f"❌ Registration failed: {response.text}")

    # Test 2: Login and get token
    print("\n2. Logging in to get token...")

    response = requests.post(
        f"{base_url}/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful! Token received.")
    else:
        print(f"❌ Login failed: {response.text}")
        return

    # Test 3: Try to access admin endpoint (should fail)
    print("\n3. Trying to access admin endpoint with regular user...")

    response = requests.post(
        f"{base_url}/admin/command",
        json={"command": "test"},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 403:
        print("✅ Access denied as expected (regular user cannot access admin)")
    else:
        print(f"❌ Unexpected response: {response.status_code} - {response.text}")

    # Test 4: Try with admin user
    print("\n4. Trying with admin user...")

    admin_response = requests.post(
        f"{base_url}/auth/token",
        data={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if admin_response.status_code == 200:
        admin_token = admin_response.json()["access_token"]

        admin_cmd_response = requests.post(
            f"{base_url}/admin/command",
            json={"command": "admin_test"},
            headers={
                "Authorization": f"Bearer {admin_token}",
                "Content-Type": "application/json"
            }
        )

        if admin_cmd_response.status_code == 200:
            print("✅ Admin access successful!")
            print(f"   Response: {admin_cmd_response.json()}")
        else:
            print(f"❌ Admin access failed: {admin_cmd_response.text}")
    else:
        print(f"❌ Admin login failed: {admin_response.text}")

    print("\n🎉 Security demo completed!")

if __name__ == "__main__":
    main()


