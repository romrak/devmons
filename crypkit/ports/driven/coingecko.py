from abc import ABC, abstractmethod
from typing import Any

from crypkit.core.model import Symbol


class CoinGecko(ABC):
    @abstractmethod
    async def symbol_info(self, symbol: Symbol) -> dict[Any, Any]:
        """Retrieve information about cryptocurrency by specific symbol.

        :raises CoingeckoNotFoundError: If the cryptocurrency does not exist in coingecko.
        :raises CoingeckoNotWorkingError: When Coingecko is not working.
        """

    async def refresh(self) -> None:
        """Refresh coingecko values.

        :raises CoingeckoNotWorkingError: When Coingecko is not working.
        """
