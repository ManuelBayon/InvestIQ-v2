"""Normalized execution direction."""

from enum import StrEnum


class Side(StrEnum):
    """Buy or sell direction, independent of position and order role."""

    BUY = "BUY"
    SELL = "SELL"
