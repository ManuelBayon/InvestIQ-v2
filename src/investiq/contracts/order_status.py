"""Canonical order states, independent of broker status labels."""

from enum import StrEnum


class OrderStatus(StrEnum):
    """Observed order state, not the result of a command.

    Partial execution is represented by quantity fields, not a separate state.
    Adapters must map source notifications explicitly; INACTIVE must never be
    interpreted as REJECTED without evidence of an order rejection.
    This vocabulary does not define allowed lifecycle transitions.
    """

    # Acceptance for execution has not yet been confirmed.
    PENDING_SUBMIT = "PENDING_SUBMIT"

    # Accepted but awaiting an activation condition.
    HELD = "HELD"

    # Active, possibly with prior partial executions.
    WORKING = "WORKING"

    # Cancellation is pending; further executions remain possible.
    PENDING_CANCEL = "PENDING_CANCEL"

    # Cancellation of the unexecuted remainder has been confirmed.
    CANCELLED = "CANCELLED"

    # The order has been reported as fully executed.
    FILLED = "FILLED"

    # Rejection of the order itself has been explicitly established.
    REJECTED = "REJECTED"

    # Inactive without sufficient information to establish a specific cause.
    INACTIVE = "INACTIVE"
