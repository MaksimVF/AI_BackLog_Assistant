




import requests
import json

BASE_URL = "http://localhost:8001/third-level"

def test_decision_recommendation():
    """Test getting decision recommendations"""
    url = f"{BASE_URL}/recommend"
    payload = {
        "triggered_by": "test_user"
    }

    response = requests.post(url, json=payload)
    print(f"Decision recommendation response: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response.json()

def test_get_results():
    """Test getting results for a run"""
    url = f"{BASE_URL}/results/1"  # Assuming run with id 1 exists
    response = requests.get(url)
    print(f"Get results response: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response.json()

def test_scenario_simulation():
    """Test scenario simulation"""
    url = f"{BASE_URL}/scenario"
    payload = {
        "tasks": [
            {"id": "task_123", "title": "Task 1", "value": 10.0, "effort": 3.0},
            {"id": "task_456", "title": "Task 2", "value": 6.0, "effort": 4.0},
            {"id": "task_789", "title": "Task 3", "value": 2.0, "effort": 5.0}
        ],
        "changes": [
            {
                "action": "drop",
                "task_id": "task_123"
            },
            {
                "action": "accelerate",
                "task_id": "task_456",
                "delta_value": 2.0,
                "delta_effort": -1.0
            }
        ]
    }

    response = requests.post(url, json=payload)
    print(f"Scenario simulation response: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response.json()

def test_confirm_decision():
    """Test confirming a decision"""
    url = f"{BASE_URL}/confirm/1"  # Assuming result with id 1 exists
    payload = {
        "decision": "accepted",
        "feedback": "Looks good"
    }

    response = requests.post(url, json=payload)
    print(f"Confirm decision response: {response.status_code}")
    print(f"Response body: {response.json()}")
    return response.json()

if __name__ == "__main__":
    print("Testing Third Level API...")

    print("\n1. Testing decision recommendation:")
    test_decision_recommendation()

    print("\n2. Testing get results:")
    test_get_results()

    print("\n3. Testing scenario simulation:")
    test_scenario_simulation()

    print("\n4. Testing confirm decision:")
    test_confirm_decision()

    print("\nAll tests completed!")



