from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from crypkit.core.model import CryptoCurrency


class CreateRequest(BaseModel):
    id_: UUID
    symbol: str


class UpdateRequest(BaseModel):
    id_: UUID
    symbol: str


class CrudOperations(ABC):
    @abstractmethod
    async def create(self, request: CreateRequest) -> CryptoCurrency:
        """Create new CryptoCurrency.

        :raises CoingeckoNotFoundError: If the cryptocurrency does not exist in coingecko.
        :raises CoingeckoNotWorkingError: When Coingecko is not working.
        """

    @abstractmethod
    async def read(self) -> list[CryptoCurrency]:
        """List all CryptoCurrencies."""

    @abstractmethod
    async def update(self, request: UpdateRequest) -> CryptoCurrency:
        """Update CryptoCurrency.

        :raises CoingeckoNotFoundError: If the cryptocurrency does not exist in coingecko.
        :raises CoingeckoNotWorkingError: When Coingecko is not working.
        """

    @abstractmethod
    async def delete(self, id_: UUID) -> None:
        """Delete CryptoCurrency.

        :raises NotFoundError: If the cryptocurrency does not exist.
        """
