from datetime import datetime

from investiq.features.features import Feature


def print_trace(
        symbol: str,
        ts: datetime,
        step: int,
        eligible_before: list[Feature],
        current: Feature,
        emit: bool,
        emitted: set[Feature],
        successors: list[Feature],
        eligible_after: list[Feature]
) -> None:
    print(
        f"\nFeature update trace :"
        f"\nSymbol = {symbol}"
        f"\nTimestamp = {ts}"
        f"\nStep = {step}"
        f"\neligible before: {[e.name for e in eligible_before]}"
        f"\ncurrent: {current.name}"
        f"\nemit: {emit}"
        f"\nemitted: {[e.name for e in emitted]}"
        f"\nsuccessors: {[s.name for s in successors]}"
        f"\neligible after : {[e.name for e in eligible_after]}"
    )