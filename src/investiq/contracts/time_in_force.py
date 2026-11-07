"""Explicit requested order validity."""

from enum import StrEnum


class TimeInForce(StrEnum):
    """Validity policy; permitted trading sessions are configured separately."""

    # Valid for the applicable trading day, as defined by the destination.
    DAY = "DAY"

    # Remains valid until cancelled, subject to destination validity limits.
    GTC = "GTC"
