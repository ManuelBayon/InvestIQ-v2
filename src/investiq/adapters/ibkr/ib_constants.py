from enum import IntEnum


class IBTickType(IntEnum):
    LAST_PRICE = 4
    DELAYED_LAST_PRICE = 68

TRADE_TICK_TYPES = {
    IBTickType.LAST_PRICE,
    IBTickType.DELAYED_LAST_PRICE
}