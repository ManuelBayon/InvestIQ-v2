from investiq.events.market_data import TradeReceived

class InMemoryTradeStore:
    """
    In memory trade store.

    TradeReceived events are supposed to be ordered by timestamp for each symbol.
    """

    def __init__(self):
        self._trades_by_symbol: dict[str, list[TradeReceived]] = {}


    def append(self, event: TradeReceived) -> None:
        symbol = event.symbol

        if symbol in self._trades_by_symbol:
            last = self._trades_by_symbol[event.symbol][-1]

            if event.timestamp_utc < last.timestamp_utc:
                raise ValueError(
                    f"timestamp_utc for symbol={event.symbol}, "
                    f"is decreasing."
                )

        self._trades_by_symbol.setdefault(symbol, []).append(event)


    @property
    def symbols(self) -> tuple[str, ...]:
        return tuple(self._trades_by_symbol)