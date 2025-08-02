from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from ..settings import settings


class SQLSessionService:
    engine: AsyncEngine = create_async_engine(url=settings.sql_settings.get_db_url, echo=True)

    session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_maker() as session_:
            try:
                yield session_
            except Exception as _ex:
                await session_.rollback()
                raise _ex
