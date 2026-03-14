from typing import AsyncGenerator

from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.async_session import async_session as _async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session() as session:
        yield session


def get_broker() -> RabbitBroker:
    """Dependency для получения RabbitBroker в REST endpoints"""
    from app.broker.router import router  # ленивый импорт — разрывает циклическую зависимость
    return router.broker