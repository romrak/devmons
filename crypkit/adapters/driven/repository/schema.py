from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.dialects.postgresql import JSONB, UUID

metadata = MetaData()

CryptoCurrencyTable = Table(
    "cryptocurrencies",
    metadata,
    Column("id", UUID, nullable=False, primary_key=True),
    Column("symbol", String, nullable=False),
    Column("metadata", JSONB(none_as_null=True), nullable=False),
)
