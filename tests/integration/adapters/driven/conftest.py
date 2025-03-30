from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from crypkit.adapters.driven.repository.config import PostgresSettings
from crypkit.adapters.driven.repository.sqlalchemy import SqlAlchemyRepository
from crypkit.ports.driven.repository import Repository


@pytest.fixture()
async def session_maker() -> async_sessionmaker[AsyncSession]:
    settings = PostgresSettings()
    engine = create_async_engine(settings.to_url())
    return async_sessionmaker(bind=engine)


@pytest.fixture()
async def session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        yield session
        await session.commit()


@pytest.fixture()
async def repository(session: AsyncSession) -> Repository:
    return SqlAlchemyRepository(session)
