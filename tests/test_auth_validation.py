

























import pytest
from fastapi.testclient import TestClient
from api.api import app
from api.validation import TaskCreate, TaskUpdate, RunCreate, RunUpdate, ResultCreate, ResultUpdate, UserCreate, UserUpdate, UserLogin
from db.models import User
from db.repo_optimized import UserRepo
from db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

client = TestClient(app)

def test_task_validation():
    # Проверка валидации задачи
    task = TaskCreate(
        title="Test Task",
        description="Test Description",
        status="open",
        priority=3,
        due_date=datetime.now()
    )
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "open"
    assert task.priority == 3
    assert task.due_date is not None

def test_run_validation():
    # Проверка валидации запуска
    run = RunCreate(
        task_id=1,
        status="completed",
        started_at=datetime.now(),
        ended_at=datetime.now()
    )
    assert run.task_id == 1
    assert run.status == "completed"
    assert run.started_at is not None
    assert run.ended_at is not None

def test_result_validation():
    # Проверка валидации результата
    result = ResultCreate(
        task_id=1,
        data={"key": "value"},
        status="success"
    )
    assert result.task_id == 1
    assert result.data == {"key": "value"}
    assert result.status == "success"

def test_user_validation():
    # Проверка валидации пользователя
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword",
        is_active=True,
        is_admin=False
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password == "testpassword"
    assert user.is_active is True
    assert user.is_admin is False

@pytest.mark.asyncio
async def test_user_registration():
    session = await get_async_session()
    repo = UserRepo(session)
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword",
        is_active=True,
        is_admin=False
    )
    user_obj = User(**user.dict())
    await repo.create(user_obj)
    user_db = await repo.get_by_username("testuser")
    assert user_db is not None
    assert user_db.username == "testuser"
    assert user_db.email == "test@example.com"
    assert user_db.is_active is True
    assert user_db.is_admin is False

@pytest.mark.asyncio
async def test_user_authentication():
    session = await get_async_session()
    repo = UserRepo(session)
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword",
        is_active=True,
        is_admin=False
    )
    user_obj = User(**user.dict())
    await repo.create(user_obj)
    # Проверка аутентификации
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_user_authorization():
    session = await get_async_session()
    repo = UserRepo(session)
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword",
        is_active=True,
        is_admin=False
    )
    user_obj = User(**user.dict())
    await repo.create(user_obj)
    # Проверка авторизации
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Проверка доступа к защищенному ресурсу
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_admin_authorization():
    session = await get_async_session()
    repo = UserRepo(session)
    user = UserCreate(
        username="adminuser",
        email="admin@example.com",
        password="adminpassword",
        is_active=True,
        is_admin=True
    )
    user_obj = User(**user.dict())
    await repo.create(user_obj)
    # Проверка авторизации
    response = client.post("/token", data={"username": "adminuser", "password": "adminpassword"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    # Проверка доступа к защищенному ресурсу
    response = client.get("/users/admin", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Admin info"





























