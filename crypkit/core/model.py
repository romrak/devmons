from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class Symbol:
    chars: str


@dataclass(frozen=True)
class CryptoId:
    id_: UUID


@dataclass(frozen=True)
class CryptoCurrencyMemento:
    id_: str
    symbol: str
    metadata: dict[Any, Any]


class CryptoCurrency:
    id_: CryptoId
    symbol: Symbol
    metadata: dict[Any, Any]

    def __init__(self, id_: CryptoId, symbol: Symbol, metadata: dict[Any, Any]) -> None:
        self.id_ = id_
        self.symbol = symbol
        self.metadata = metadata

    def memento(self) -> CryptoCurrencyMemento:
        return CryptoCurrencyMemento(
            str(self.id_.id_), self.symbol.chars, self.metadata
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CryptoCurrency):
            return self.id_ == other.id_
        return False

    def __hash__(self) -> int:
        return hash(self.id_)

    def __str__(self) -> str:
        return f"{self.id_} {self.symbol}"

    def __repr__(self) -> str:
        return f"{self.id_} {self.symbol}"
