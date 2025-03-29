from uuid import UUID

from crypkit.core.model import CryptoId, Symbol
from crypkit.ports.driven.coingecko import CoinGecko
from crypkit.ports.driven.repository import UnitOfWork
from crypkit.ports.driving.crud import CreateRequest, CrudOperations, CryptoCurrency, UpdateRequest


class CryptoService(CrudOperations):
    def __init__(self, unit_of_work: UnitOfWork, coin_gecko: CoinGecko) -> None:
        self._uow = unit_of_work
        self._coin_gecko = coin_gecko

    async def create(self, request: CreateRequest) -> CryptoCurrency:
        info = await self._coin_gecko.symbol_info(request.symbol)
        async with self._uow as repository:
            return await repository.save(
                CryptoCurrency(id_=CryptoId(request.id_), symbol=Symbol(request.symbol), metadata=info)
            )

    async def read(self) -> list[CryptoCurrency]:
        async with self._uow as repository:
            return await repository.load_all()

    async def update(self, request: UpdateRequest) -> CryptoCurrency:
        info = await self._coin_gecko.symbol_info(request.symbol)
        async with self._uow as repository:
            return await repository.update(
                CryptoCurrency(id_=CryptoId(request.id_), symbol=Symbol(request.symbol), metadata=info)
            )

    async def delete(self, id_: UUID) -> None:
        async with self._uow as repository:
            return await repository.delete(CryptoId(id_))
