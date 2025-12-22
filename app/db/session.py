from typing import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from app.core.config import settings

# Create async engine and session factory
async_engine = create_async_engine(str(settings.DB_URL), echo=False, future=True, pool_size=settings.DB_POOL_SIZE, max_overflow=settings.DB_MAX_OVERFLOW, pool_timeout=settings.DB_POOL_TIMEOUT, pool_recycle=settings.DB_POOL_RECYCLE)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Create sync engine for synchronous operations
sync_db_url = str(settings.DB_URL).replace("postgresql+asyncpg", "postgresql")
sync_engine = create_engine(sync_db_url, pool_size=settings.DB_POOL_SIZE, max_overflow=settings.DB_MAX_OVERFLOW, pool_timeout=settings.DB_POOL_TIMEOUT, pool_recycle=settings.DB_POOL_RECYCLE)
sync_session = sessionmaker(bind=sync_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields an AsyncSession."""
    async with async_session() as session:
        yield session


def get_db_sync() -> Generator[Session, None, None]:
    """Dependency that yields a synchronous Session."""
    db = sync_session()
    try:
        yield db
    finally:
        db.close()
