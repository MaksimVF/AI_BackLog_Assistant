



from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database URL from environment variable or default
DATABASE_URL = "sqlite+aiosqlite:///site.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()

# Dependency to get async session
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()



