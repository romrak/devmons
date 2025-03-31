import logging
from uuid import UUID

from crypkit.core.model import CryptoCurrency, CryptoId, Symbol
from crypkit.ports.driven.coingecko import CoinGecko
from crypkit.ports.driven.repository import UnitOfWork
from crypkit.ports.driving.crud import CreateDTO, CrudOperations, UpdateDTO
from crypkit.ports.driving.refresh import Refresh

logger = logging.getLogger(__name__)


class CryptoService(CrudOperations, Refresh):
    def __init__(self, unit_of_work: UnitOfWork, coin_gecko: CoinGecko) -> None:
        self._uow = unit_of_work
        self._coin_gecko = coin_gecko

    async def create(self, request: CreateDTO) -> CryptoCurrency:
        logger.info(f"Creating new cryptocurrency: {request}")
        info = await self._coin_gecko.symbol_info(Symbol(request.symbol))
        async with self._uow as repository:
            return await repository.save(
                CryptoCurrency(
                    id_=CryptoId(request.id),
                    symbol=Symbol(request.symbol),
                    metadata=info,
                )
            )

    async def read(self) -> list[CryptoCurrency]:
        logger.info("Reading all cryptocurrencies")
        async with self._uow as repository:
            return await repository.load_all()

    async def update(self, request: UpdateDTO) -> CryptoCurrency:
        logger.info(f"Updating cryptocurrency: {request}")
        info = await self._coin_gecko.symbol_info(Symbol(request.symbol))
        async with self._uow as repository:
            return await repository.update(
                CryptoCurrency(
                    id_=CryptoId(request.id),
                    symbol=Symbol(request.symbol),
                    metadata=info,
                )
            )

    async def delete(self, id_: UUID) -> None:
        logger.info(f"Deleting cryptocurrency: {id_}")
        async with self._uow as repository:
            return await repository.delete(CryptoId(id_))

    async def refresh(self) -> None:
        logger.info("Refreshing cryptocurrencies")
        await self._coin_gecko.refresh()
