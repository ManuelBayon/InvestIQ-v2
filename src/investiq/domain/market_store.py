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
    TradeReceived are stored by symbol.
    """

    def __init__(self):
        self._trades: dict[str, list[TradeReceived]] = {}


    def on_trade_received(self, event: TradeReceived) -> None:
        symbol = event.symbol
        if symbol in self._trades:
            last = self._trades[event.symbol][-1]

            if event.timestamp_utc < last.timestamp_utc:
                raise ValueError(
                    f"event.timestamp_utc={event.timestamp_utc} < last.timestamp_utc={last.timestamp_utc}"
                )

        self._trades.setdefault(symbol, []).append(event)