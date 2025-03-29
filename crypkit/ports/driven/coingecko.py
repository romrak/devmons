from abc import ABC

from crypkit.core.model import Symbol


class CoinGecko(ABC):
    @staticmethod
    async def symbol_info(self, symbol: Symbol) -> dict:
        """Retrieve information about cryptocurrency by specific symbol.

        :raises CoingeckoNotFoundError: If the cryptocurrency does not exist in coingecko.
        :raises CoingeckoNotWorkingError: When Coingecko is not working.
        """
