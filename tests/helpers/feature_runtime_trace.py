from datetime import datetime

from investiq.features.feature_runtime import Node


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
        f"\nFeature update trace :"
        f"\nSymbol = {symbol}"
        f"\nTimestamp = {ts}"
        f"\nStep = {step}"
        f"\neligible before: {[e.type.name for e in eligible_before]}"
        f"\ncurrent: {current.type.name}"
        f"\nemit: {emit}"
        f"\nemitted: {[e.type.name for e in emitted]}"
        f"\nsuccessors: {[s.type.name for s in successors]}"
        f"\neligible after : {[e.type.name for e in eligible_after]}"
    )