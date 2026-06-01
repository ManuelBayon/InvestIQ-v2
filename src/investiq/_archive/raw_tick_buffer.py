from investiq.domain.models import RawTick


class RawTickBuffer:

    def __init__(self):
        self._buffer: dict[str, list[RawTick]] = {}

    def enqueue(self, raw_ticks: dict[str, list[RawTick]]) -> None:
        """
        2026-05-28:
        Enqueue raw tick list for each symbol.
        """
        for _symbol, raw_tick_list in raw_ticks.items():
            if _symbol not in self._buffer.keys():
                self._buffer[_symbol] = []
            self._buffer[_symbol].extend(raw_tick_list)

    def dequeue(
            self,
            symbol: str,
            n: int
    ) -> tuple[RawTick, ...]:
        """
        2026-05-28:
        Select, delete and return an immuable view of the n first RawTicks.
        """
        selected = self._buffer[symbol][:n]
        del self._buffer[symbol][:n]
        if not self._buffer[symbol]:
            del self._buffer[symbol]
        return tuple(selected)

    def pending_symbols(self) -> set[str]:
        """
        2026-05-28:
        Return symbol that have pending RawTicks.
        """
        return set(self._buffer.keys())

    def get_individual_buffer_size(self, symbol: str) -> int:
        if symbol not in self.pending_symbols():
            raise ValueError(
                f"symbol={symbol} is not available, "
                f"registered symbols are:={self.pending_symbols()}"
            )
        return len(self._buffer[symbol])