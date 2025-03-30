import uuid
from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from crypkit.adapters.driven.repository.schema import CryptoCurrencyTable
from crypkit.adapters.driven.repository.sqlalchemy import SqlAlchemyRepository
from tests.unit.ports.driven.test_repository import RepositoryTest


class TestSqlAlchemyRepository(RepositoryTest):
    @pytest.fixture(autouse=True)
    async def setup(
        self, session: AsyncSession, repository: SqlAlchemyRepository
    ) -> None:
        """Store session and repository instance."""
        self._session = session
        self._repository = repository

    async def empty(self) -> None:
        await self._session.execute(text("truncate table cryptocurrencies"))

    async def insert(self, row: dict[str, Any]) -> None:
        await self._session.execute(insert(CryptoCurrencyTable).values(**row))

    async def load_by_id(self, id_: uuid.UUID) -> tuple[uuid.UUID, str, dict[str, Any]]:
        result = await self._session.execute(
            text("select * from cryptocurrencies where id = :id"), {"id": id_}
        )
        row = result.mappings().__next__()
        return row["id"], row["symbol"], row["metadata"]

    async def load_all(self) -> list[tuple[uuid.UUID, str, dict[str, Any]]]:
        result = await self._session.execute(text("select * from cryptocurrencies"))
        rows = []
        for row in result.mappings():
            rows.append((row["id"], row["symbol"], row["metadata"]))
        return rows

    async def repository(self) -> SqlAlchemyRepository:
        return self._repository
