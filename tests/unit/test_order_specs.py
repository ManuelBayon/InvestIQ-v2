import pytest

from investiq.domain.orders import BracketOrderSpec, LimitOrderSpec, MarketOrderSpec, StopOrderSpec


@pytest.mark.parametrize("entry_side,exit_side", [("BUY", "SELL"), ("SELL", "BUY")])
def test_bracket_has_complete_individual_specs(entry_side, exit_side):
    bracket = BracketOrderSpec(
        entry=MarketOrderSpec(side=entry_side, quantity=2, tif="DAY"),
        stop_loss=StopOrderSpec(side=exit_side, quantity=2, tif="GTC", stop_price=95),
        take_profit=LimitOrderSpec(side=exit_side, quantity=2, tif="DAY", limit_price=105),
    )
    assert bracket.stop_loss.tif == "GTC"
    assert bracket.take_profit.quantity == 2


@pytest.mark.parametrize("quantity", [0, -1, float("nan"), float("inf")])
def test_invalid_quantity_is_rejected(quantity):
    with pytest.raises(ValueError, match="quantity"):
        MarketOrderSpec(side="BUY", quantity=quantity, tif="DAY")


@pytest.mark.parametrize("side,quantity", [("BUY", 1), ("SELL", 2)])
def test_v1_rejects_inconsistent_exit(side, quantity):
    with pytest.raises(ValueError, match="V1 exits"):
        BracketOrderSpec(
            entry=MarketOrderSpec(side="BUY", quantity=1, tif="DAY"),
            stop_loss=StopOrderSpec(side=side, quantity=quantity, tif="DAY", stop_price=95),
        )
