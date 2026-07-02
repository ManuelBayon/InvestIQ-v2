from typing import runtime_checkable, Protocol

from investiq.domain.market_data.contracts.store import TMarketEvent


@runtime_checkable
class MarketStoreReader(Protocol):

    def window(self, symbol: str, n: int) -> tuple[TMarketEvent, ...]:
        ...

    def symbols(self) -> set[str]:
        ...

    def has_at_least(self, symbol: str, n: int) -> bool:
        ...