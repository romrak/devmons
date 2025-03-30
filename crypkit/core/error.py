class NotFoundError(Exception):
    """Raised when cryptocurrency is not found in repository."""


class DuplicityError(Exception):
    """Raised when one cryptocurrency with id is already in repository."""


class CoingeckoNotFoundError(Exception):
    """Raised when cryptocurrency is not found in Coingecko."""


class CoingeckoNotWorkingError(Exception):
    """Raised when Coingecko is not operational."""
