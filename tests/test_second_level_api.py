

















import pytest
from httpx import AsyncClient
from level2.api.second_level_api import app
from level2.db.models_second_level import init_db, async_session

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    await init_db()

@pytest.mark.asyncio
async def test_create_task(client):
    response = await client.post("/tasks", json={"title": "Test Task", "value": 10, "effort": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["value"] == 10
    assert data["effort"] == 5

@pytest.mark.asyncio
async def test_get_tasks(client):
    response = await client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_run(client):
    response = await client.post("/runs", json={"triggered_by": "user1", "modules": ["prioritization", "analytics"]})
    assert response.status_code == 200
    data = response.json()
    assert data["triggered_by"] == "user1"
    assert data["modules"] == ["prioritization", "analytics"]

@pytest.mark.asyncio
async def test_get_runs(client):
    response = await client.get("/runs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_result(client):
    # First create a task and a run
    task_response = await client.post("/tasks", json={"title": "Test Task", "value": 10, "effort": 5})
    task_id = task_response.json()["id"]

    run_response = await client.post("/runs", json={"triggered_by": "user1", "modules": ["prioritization"]})
    run_id = run_response.json()["id"]

    # Now create a result
    response = await client.post("/results", json={
        "run_id": run_id,
        "module_name": "prioritization",
        "task_id": task_id,
        "result": {"priority": "must-have", "score": 8.7}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["module_name"] == "prioritization"
    assert data["result"]["priority"] == "must-have"

@pytest.mark.asyncio
async def test_get_results_for_task(client):
    # First create a task
    task_response = await client.post("/tasks", json={"title": "Test Task", "value": 10, "effort": 5})
    task_id = task_response.json()["id"]

    response = await client.get(f"/results/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


















