from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.core.config import settings
from app.database.models.base import Base


engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False
)
SessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор асинхронной сессии БД для Dependency Injection.
    """
    async with SessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Создание всех таблиц в базе данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """
    Удаление всех таблиц в базе данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
