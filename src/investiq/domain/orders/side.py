from enum import StrEnum


class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"

class TimeInForce(StrEnum):
    DAY = "DAY"
    GTC = "GTC"
    IOC = "IOC"
    GTD = "GTD"
    OPG = "OPG"
    FOK = "FOK"
    DTC = "DTC"

