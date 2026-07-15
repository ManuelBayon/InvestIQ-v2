from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from investiq.events.trade_received import TradeReceived

@dataclass(frozen=True)
class LatestTradeSnapshot:
    latest: Mapping[str, Decimal]


class InMemoryMarketStore:
    """
    In memory trade store.

    TradeReceived events are supposed to be ordered by timestamp for each symbol.
    """

    def __init__(self):
        self._trades_by_symbol: dict[str, list[TradeReceived]] = {}


    def on_trade_received(self, event: TradeReceived) -> None:
        symbol = event.symbol
        if symbol in self._trades_by_symbol:
            last = self._trades_by_symbol[event.symbol][-1]

            if event.timestamp_utc < last.timestamp_utc:
                raise ValueError(
                    f"timestamp_utc for symbol={event.symbol}, is decreasing."
                )

        self._trades_by_symbol.setdefault(symbol, []).append(event)