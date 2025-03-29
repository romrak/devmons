from abc import ABC, abstractmethod

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
        """Save cryptocurrency to database."""

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
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Commit or rollback the transaction."""
        pass
