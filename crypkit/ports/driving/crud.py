from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from crypkit.core.model import CryptoCurrency


@dataclass(frozen=True)
class CreateDTO:
    id: UUID
    symbol: str


@dataclass(frozen=True)
class UpdateDTO:
    id: UUID
    symbol: str


class CrudOperations(ABC):
    @abstractmethod
    async def create(self, request: CreateDTO) -> CryptoCurrency:
        """Create new CryptoCurrency.

        :raises CoingeckoNotFoundError: If the cryptocurrency does not exist in coingecko.
        :raises CoingeckoNotWorkingError: When Coingecko is not working.
        """

    @abstractmethod
    async def read(self) -> list[CryptoCurrency]:
        """List all CryptoCurrencies."""

    @abstractmethod
    async def update(self, request: UpdateDTO) -> CryptoCurrency:
        """Update CryptoCurrency.

        :raises CoingeckoNotFoundError: If the cryptocurrency does not exist in coingecko.
        :raises CoingeckoNotWorkingError: When Coingecko is not working.
        """

    @abstractmethod
    async def delete(self, id_: UUID) -> None:
        """Delete CryptoCurrency.

        :raises NotFoundError: If the cryptocurrency does not exist.
        """
