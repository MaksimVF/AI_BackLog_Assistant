
















from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Numeric, JSON
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# --- Таблица задач ---
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), nullable=True)  # ID из Jira/Trello и т.д.
    title = Column(Text, nullable=False)
    status = Column(String(50), nullable=True)
    value = Column(Numeric, nullable=True)
    effort = Column(Numeric, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    results = relationship("SecondLevelResult", back_populates="task")


# --- Таблица запусков пайплайна ---
class SecondLevelRun(Base):
    __tablename__ = "second_level_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_at = Column(DateTime, default=datetime.utcnow)
    triggered_by = Column(String(255), nullable=True)  # кто запустил
    modules = Column(JSON, nullable=True)
    status = Column(String(50), default="completed")

    results = relationship("SecondLevelResult", back_populates="run")


# --- Таблица результатов анализа ---
class SecondLevelResult(Base):
    __tablename__ = "second_level_results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("second_level_runs.id", ondelete="CASCADE"))
    module_name = Column(String(100), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    run = relationship("SecondLevelRun", back_populates="results")
    task = relationship("Task", back_populates="results")


# --- Создание асинхронного движка и сессии ---
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/mydb"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


# --- Утилита для инициализации базы ---
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
















