from uuid import UUID

from sqlalchemy import RowMapping, delete, exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from crypkit.adapters.driven.repository.schema import CryptoCurrencyTable
from crypkit.core.error import DuplicityError, NotFoundError
from crypkit.core.model import CryptoCurrency, CryptoId
from crypkit.ports.driven.repository import Repository


class SqlAlchemyRepository(Repository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def load_all(self) -> list[CryptoCurrency]:
        rows = await self._session.execute(
            select(CryptoCurrencyTable).order_by(CryptoCurrencyTable.c.id)
        )
        result = []
        for row in rows.mappings():
            result.append(self._row_to_crypto_currency(row))
        return result

    async def delete(self, crypto_id: CryptoId) -> None:
        if not await self._row_exists(crypto_id.id_):
            raise NotFoundError()

        await self._session.execute(
            delete(CryptoCurrencyTable).where(CryptoCurrencyTable.c.id == crypto_id.id_)
        )

    async def save(self, crypto_currency: CryptoCurrency) -> CryptoCurrency:
        memento = crypto_currency.memento()
        if await self._row_exists(memento.id_):
            raise DuplicityError()

        await self._session.execute(
            insert(CryptoCurrencyTable).values(
                {
                    "id": memento.id_,
                    "symbol": memento.symbol,
                    "metadata": memento.metadata,
                }
            )
        )
        return crypto_currency

    async def update(self, crypto_currency: CryptoCurrency) -> CryptoCurrency:
        memento = crypto_currency.memento()
        if not await self._row_exists(memento.id_):
            raise NotFoundError()

        await self._session.execute(
            update(CryptoCurrencyTable)
            .values(
                {
                    "id": memento.id_,
                    "symbol": memento.symbol,
                    "metadata": memento.metadata,
                }
            )
            .where(CryptoCurrencyTable.c.id == memento.id_)
        )
        return crypto_currency

    @staticmethod
    def _row_to_crypto_currency(row: RowMapping) -> CryptoCurrency:
        return CryptoCurrency(
            id_=CryptoId(row["id"]),
            symbol=row["symbol"],
            metadata=row["metadata"],
        )

    async def _row_exists(self, id_: str | UUID) -> bool:
        row_exists = await self._session.execute(
            select(exists().where(CryptoCurrencyTable.c.id == id_))
        )
        return bool(row_exists.scalar())
