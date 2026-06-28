from dataclasses import dataclass

from investiq.events.market_data import TradeReceived

@dataclass(frozen=True)
class SMA:
    """
    Preconditions:
        - The caller passes exactly `window` trades.
        - All trades belong to the same instrument.

    This calculator is pure and does not perform orchestration.
    """

    window: int

    def calculate(self, events: tuple[TradeReceived, ...]) -> float:
        if len(events) != self.window:
            raise ValueError(
                f"window != len(events), "
                f"window={self.window}, "
                f"len(events)={len(events)}."
            )

        return sum(e.price for e in events) / len(events)