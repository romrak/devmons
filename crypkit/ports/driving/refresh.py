from abc import ABC, abstractmethod


class Refresh(ABC):
    @abstractmethod
    async def refresh(self) -> None:
        """Refresh all the cryptocurrencies."""
