"""Resolve canonical symbols to configured IBKR contracts."""

from collections.abc import Mapping
from copy import deepcopy

from ib_insync import Contract


class IBKRInstruments:
    """Hold the configured IBKR contract for each canonical symbol."""

    def __init__(self, contracts: Mapping[str, Contract]) -> None:
        self._contracts = {
            symbol: deepcopy(contract)
            for symbol, contract in contracts.items()
        }

    def resolve(self, symbol: str) -> Contract:
        """Return an independent contract for the exact canonical symbol."""
        try:
            contract = self._contracts[symbol]
        except KeyError:
            raise KeyError(f"No IBKR contract configured for {symbol!r}") from None
        return deepcopy(contract)
