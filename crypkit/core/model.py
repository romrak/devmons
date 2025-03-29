from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Symbol:
    chars: str

@dataclass(frozen=True)
class CryptoId:
    id_: UUID

class CryptoCurrency:
    id_: CryptoId
    symbol: Symbol
    metadata: dict

    def __init__(self, id_: CryptoId, symbol: Symbol, metadata: dict) -> None:
        self.id_ = id_
        self.symbol = symbol
        self.metadata = metadata

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def __str__(self):
        return f"{self.id_} {self.symbol}"

    def __repr__(self):
        return f"{self.id_} {self.symbol}"