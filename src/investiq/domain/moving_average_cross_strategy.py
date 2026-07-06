from investiq.domain.base_strategy import DecisionSnapshot, TradingIntent


class MovingAverageCrossStrategy:

    def decide(
            self,
            snapshot: DecisionSnapshot
    ) -> list[TradingIntent]:
        ...