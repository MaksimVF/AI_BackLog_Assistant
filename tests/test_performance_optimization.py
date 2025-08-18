























import pytest
from fastapi.testclient import TestClient
from api.api import app
from db.repo_optimized import TaskRepo, RunRepo, ResultRepo
from db.models import Task, Run, Result
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_async_session
import time

client = TestClient(app)

@pytest.mark.asyncio
async def test_task_repo_performance():
    session = await get_async_session()
    repo = TaskRepo(session)
    start_time = time.time()
    tasks = await repo.get_all()
    end_time = time.time()
    assert end_time - start_time < 1.0  # Должно выполняться менее чем за 1 секунду

@pytest.mark.asyncio
async def test_run_repo_performance():
    session = await get_async_session()
    repo = RunRepo(session)
    start_time = time.time()
    runs = await repo.get_all()
    end_time = time.time()
    assert end_time - start_time < 1.0  # Должно выполняться менее чем за 1 секунду

@pytest.mark.asyncio
async def test_result_repo_performance():
    session = await get_async_session()
    repo = ResultRepo(session)
    start_time = time.time()
    results = await repo.get_all()
    end_time = time.time()
    assert end_time - start_time < 1.0  # Должно выполняться менее чем за 1 секунду

def test_api_performance():
    start_time = time.time()
    response = client.get("/tasks")
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 1.0  # Должно выполняться менее чем за 1 секунду

def test_api_gzip():
    response = client.get("/tasks", headers={"Accept-Encoding": "gzip"})
    assert response.status_code == 200
    assert "content-encoding" in response.headers
    assert response.headers["content-encoding"] == "gzip"



























