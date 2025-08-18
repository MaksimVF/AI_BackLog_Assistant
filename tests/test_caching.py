
























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
async def test_task_caching():
    session = await get_async_session()
    repo = TaskRepo(session)
    # Создаем задачу
    task = Task(title="Test Task", description="Test Description")
    await repo.create(task)
    # Получаем задачи дважды и проверяем, что второй запрос быстрее
    start_time = time.time()
    tasks1 = await repo.get_all()
    end_time = time.time()
    first_request_time = end_time - start_time

    start_time = time.time()
    tasks2 = await repo.get_all()
    end_time = time.time()
    second_request_time = end_time - start_time

    assert second_request_time < first_request_time

@pytest.mark.asyncio
async def test_run_caching():
    session = await get_async_session()
    repo = RunRepo(session)
    # Создаем запуск
    run = Run(task_id=1, status="completed")
    await repo.create(run)
    # Получаем запуски дважды и проверяем, что второй запрос быстрее
    start_time = time.time()
    runs1 = await repo.get_all()
    end_time = time.time()
    first_request_time = end_time - start_time

    start_time = time.time()
    runs2 = await repo.get_all()
    end_time = time.time()
    second_request_time = end_time - start_time

    assert second_request_time < first_request_time

@pytest.mark.asyncio
async def test_result_caching():
    session = await get_async_session()
    repo = ResultRepo(session)
    # Создаем результат
    result = Result(task_id=1, data={"key": "value"})
    await repo.create(result)
    # Получаем результаты дважды и проверяем, что второй запрос быстрее
    start_time = time.time()
    results1 = await repo.get_all()
    end_time = time.time()
    first_request_time = end_time - start_time

    start_time = time.time()
    results2 = await repo.get_all()
    end_time = time.time()
    second_request_time = end_time - start_time

    assert second_request_time < first_request_time

def test_api_caching():
    # Создаем задачу
    response = client.post("/tasks", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    # Получаем задачи дважды и проверяем, что второй запрос быстрее
    start_time = time.time()
    response1 = client.get("/tasks")
    end_time = time.time()
    first_request_time = end_time - start_time

    start_time = time.time()
    response2 = client.get("/tasks")
    end_time = time.time()
    second_request_time = end_time - start_time

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert second_request_time < first_request_time

def test_api_cache_invalidation():
    # Создаем задачу
    response = client.post("/tasks", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    # Получаем задачи
    response1 = client.get("/tasks")
    assert response1.status_code == 200
    # Обновляем задачу
    task_id = response1.json()[0]["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task"})
    assert response.status_code == 200
    # Получаем задачи снова и проверяем, что данные обновлены
    response2 = client.get("/tasks")
    assert response2.status_code == 200
    assert response2.json()[0]["title"] == "Updated Task"




























