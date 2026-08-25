from datetime import datetime

from investiq.domain.features.feature_runtime import Node


def print_trace(
        symbol: str,
        ts: datetime,
        step: int,
        eligible_before: list[Node],
        current: Node,
        emit: bool,
        emitted: set[Node],
        successors: list[Node],
        eligible_after: list[Node]
) -> None:
    print(
        f"\n  ————————————  FEATURE RUNTIME TRACE  ————————————  \n"
        f"\nSymbol = {symbol}"
        f"\nTimestamp = {ts}"
        f"\nStep = {step}"
        f"\n\neligible before: {[e for e in eligible_before]}"
        f"\n\ncurrent: {current}"
        f"\n\nemit: {emit}"
        f"\n\nemitted: {[e for e in emitted]}"
        f"\n\nsuccessors: {[s for s in successors]}"
        f"\n\neligible after : {[e for e in eligible_after]}"
    )