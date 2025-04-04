from abc import ABC, abstractmethod
from typing import Any

from crypkit.core.model import CryptoCurrency, CryptoId


class Repository(ABC):
    @abstractmethod
    async def load_all(self) -> list[CryptoCurrency]:
        """Load all cryptocurrencies."""

    @abstractmethod
    async def delete(self, crypto_id: CryptoId) -> None:
        """Delete cryptocurrency by id.

        :raises NotFoundError: If the cryptocurrency does not exist.
        """

    @abstractmethod
    async def save(self, crypto_currency: CryptoCurrency) -> CryptoCurrency:
        """Save cryptocurrency to database.

        :raises DuplicityError: If the cryptocurrency already exists.
        """

    @abstractmethod
    async def update(self, crypto_currency: CryptoCurrency) -> CryptoCurrency:
        """Update cryptocurrency by id.

        :raises NotFoundError: If the cryptocurrency does not exist.
        """


class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> "Repository":
        """Start a transaction and return repository."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Commit or rollback the transaction."""
        pass
