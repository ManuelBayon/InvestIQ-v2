from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum, auto

from investiq.domain.models import Bar, RawTick
from investiq._archive.raw_tick_buffer import RawTickBuffer


@dataclass
class WorkingBar:
    open_timestamp_utc: datetime | None = None # at open
    open: float | None = None # at open
    high: float | None = None # update if needed
    low: float  | None = None # update if needed
    close: float | None = None # update at each tick
    volume: float = 0.0 # update at each tick


class _STATE(StrEnum):
    INIT = auto()
    WARMUP = auto()
    NEW_BAR = auto()
    ACTIVE = auto()
    BAR_AVAILABLE = auto()


class TickAggregator:

    def __init__(
            self,
            raw_tick_buffer: RawTickBuffer,
            bar_size: str = "1 min",
    ):
        """
         barSizeSetting: Must be one of: '1 min', '5 mins'.
        """
        if not bar_size in ['1 min', '5 mins']:
            raise ValueError("bar_size_settings must be one of: 1min, 5min")
        self._raw_tick_buffer = raw_tick_buffer
        self.bar_size = bar_size
        self._bar_state: dict[str, _STATE] = {}
        self._working_bar: dict[str, WorkingBar] = {}

    def _is_new_minute(
            self,
            reference_ts_utc: datetime,
            current_ts_utc: datetime,
    ) -> bool:
        diff_minute = format(reference_ts_utc, "%M") != format(current_ts_utc, "%M")
        return diff_minute

    def _is_new_bar(
            self,
            reference: datetime,
            current: datetime
    ) -> bool:
        """
        bar_size parameter is checked at init should not raise an error.
        """
        match self.bar_size:
            case "1 min":
                return current - reference >= timedelta(minutes=1)
            case "5 mins":
                return (current - reference) >= timedelta(minutes=5)

    def _start_new_working_bar(self, working_bar: WorkingBar, tick: RawTick) -> None:
        working_bar.open_timestamp_utc = tick.timestamp_utc
        working_bar.open = tick.price
        working_bar.high = tick.price
        working_bar.low = tick.price
        working_bar.close = tick.price
        working_bar.volume = tick.size

    def _on_init(self, symbol: str, tick: RawTick) -> None:
        self._working_bar[symbol].open_timestamp_utc = tick.timestamp_utc
        self._bar_state[symbol] = _STATE.WARMUP
        """print(
            f"\nFor {symbol}, set reference time={tick.timestamp_utc}"
            f"\nTRANSITION from INIT to WARMUP"
        )"""

    def _on_warm_up(self, symbol: str, tick: RawTick) -> None:
        reference_time = self._working_bar[symbol].open_timestamp_utc
        current_time  =tick.timestamp_utc
        if self._is_new_minute(reference_ts_utc=reference_time, current_ts_utc=current_time):
            bar = self._working_bar[symbol]
            self._start_new_working_bar(bar, tick)
            self._bar_state[symbol] = _STATE.ACTIVE
        else:
            pass

    def _on_active_state(self, symbol: str, tick: RawTick) -> Bar | None:
        working_bar = self._working_bar[symbol]
        closed_bar = None
        if self._is_new_bar(working_bar.open_timestamp_utc, tick.timestamp_utc):
            closed_bar = Bar(
                symbol=symbol,
                timestamp_utc=working_bar.open_timestamp_utc,
                open=working_bar.open,
                high=working_bar.high,
                low=working_bar.low,
                close=working_bar.close,
                volume=int(working_bar.volume)
            )
            bar = self._working_bar[symbol]
            self._start_new_working_bar(bar, tick)
        else:
            working_bar.high = tick.price if tick.price > working_bar.high else working_bar.high
            working_bar.low = tick.price if tick.price < working_bar.low else working_bar.low
            working_bar.close = tick.price
            working_bar.volume += tick.size
        return closed_bar

    def run(self) -> list[Bar]:
        """
        """

        _closed_bars: list[Bar] = []

        for symbol in self._raw_tick_buffer.pending_symbols():

            _len_buffer = self._raw_tick_buffer.get_individual_buffer_size(symbol)
            _ticks = self._raw_tick_buffer.dequeue(symbol, _len_buffer)

            if symbol not in self._bar_state.keys():
                self._working_bar[symbol] = WorkingBar()
                self._bar_state[symbol] = _STATE.INIT

            for t in _ticks:

                if t.tick_type != 68: #tickType = 68 <=> Delayed last traded price
                    continue

                match self._bar_state[symbol]:

                    case _STATE.INIT:
                        self._on_init(symbol, t)

                    case _STATE.WARMUP:
                        self._on_warm_up(symbol, t)

                    case _STATE.ACTIVE:
                        closed_bar = self._on_active_state(symbol, t)
                        if closed_bar:
                            _closed_bars.append(closed_bar)

                    case _:
                        raise KeyError(f"Unknown _State={_STATE}")

        return _closed_bars