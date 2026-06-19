import pytest
from math import nan

from investiq.domain.instruments import InstrumentSpecs, StockSpecs
from investiq.domain.order_specs import (Side, LimitOrderSpec, BracketOrderSpec, StopMarketOrderSpec, MarketOrderSpec)

class TestMarketOrderIntent:
    def test_market_order_intent_raises_if_quantity_not_finite(self):
        with pytest.raises(ValueError):
            MarketOrderSpec(
                instrument=StockSpecs("AMD"),
                tif="DAY",
                quantity=nan,
                direction=Side.BUY,
            )
    def test_market_order_intent_raises_if_quantity_is_null(self):
        with pytest.raises(ValueError):
            MarketOrderSpec(
                instrument=StockSpecs("AMD"),
                tif="DAY",
                quantity=0,
                direction=Side.BUY
            )
    def test_market_order_intent_raises_if_quantity_is_negative(self):
        with pytest.raises(ValueError):
            MarketOrderSpec(
                instrument=StockSpecs("AMD"),
                tif="DAY",
                quantity=-1,
                direction=Side.BUY
            )
    def test_market_order_intent_valid_case(self):
        MarketOrderSpec(
            instrument=StockSpecs("AMD"),
            tif="DAY",
            quantity=1,
            direction=Side.BUY
        )

class TestLimitOrderIntent:
    def test_limit_order_intent_raises_if_quantity_not_finite(self):
        with pytest.raises(ValueError):
            LimitOrderSpec(
                quantity=nan,
                direction=Side.BUY,
                price=100.0
            )
    def test_limit_order_intent_raises_if_quantity_is_null(self):
        with pytest.raises(ValueError):
            LimitOrderSpec(
                quantity=0,
                direction=Side.BUY,
                price=100.0
            )
    def test_limit_order_intent_raises_if_quantity_is_negative(self):
        with pytest.raises(ValueError):
            LimitOrderSpec(
                quantity=-1,
                direction=Side.BUY,
                price=100.0
            )
    def test_limit_order_intent_raises_if_price_not_finite(self):
        with pytest.raises(ValueError):
            LimitOrderSpec(
                quantity=1,
                direction=Side.BUY,
                price=nan
            )
    def test_limit_order_intent_raises_if_price_is_null(self):
        with pytest.raises(ValueError):
            LimitOrderSpec(
                quantity=1,
                direction=Side.BUY,
                price=0
            )
    def test_limit_order_intent_raises_if_price_is_negative(self):
        with pytest.raises(ValueError):
            LimitOrderSpec(
                quantity=1,
                direction=Side.BUY,
                price=-1
            )
    def test_limit_order_intent_valid_case(self):
        LimitOrderSpec(
            quantity=1,
            direction=Side.BUY,
            price=100.0
        )

class TestStopMarketOrderIntent:
    def test_stop_market_order_intent_raises_if_trigger_price_not_finite(self):
        with pytest.raises(ValueError):
            StopMarketOrderSpec(
                trigger_price=nan,
                triggered_order= MarketOrderSpec(
                    instrument=StockSpecs("AMD"),
                    tif="DAY",
                    quantity=1,
                    direction=Side.BUY
                )
            )
    def test_stop_market_order_intent_raises_if_trigger_price_is_null(self):
        with pytest.raises(ValueError):
            StopMarketOrderSpec(
                trigger_price=0,
                triggered_order= MarketOrderSpec(
                    instrument=StockSpecs("AMD"),
                    tif="DAY",
                    quantity=1,
                    direction=Side.BUY
                )
            )
    def test_stop_market_order_intent_raises_if_trigger_price_is_negative(self):
        with pytest.raises(ValueError):
            StopMarketOrderSpec(
                trigger_price=-1,
                triggered_order= MarketOrderSpec(
                    instrument=StockSpecs("AMD"),
                    tif="DAY",
                    quantity=1,
                    direction=Side.BUY
                )
            )
    def test_stop_market_order_intent_valid_case(self):
        StopMarketOrderSpec(
            trigger_price=100.0,
            triggered_order=MarketOrderSpec(
                instrument=StockSpecs("AMD"),
                tif="DAY",
                quantity=1,
                direction=Side.BUY
            )
        )

class TestBracketOrderIntent:
    def test_bracket_order_intent_raises_if_no_target_profit_and_no_stop_loss(self):
        with pytest.raises(ValueError):
            BracketOrderSpec(
                entry=LimitOrderSpec(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=None,
                take_profit=None,
            )
    def test_bracket_order_intent_raises_if_stop_loss_direction_and_entry_are_same(self):
        with pytest.raises(ValueError):
            BracketOrderSpec(
                entry=LimitOrderSpec(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=[
                    StopMarketOrderSpec(
                        trigger_price=100.0,
                        triggered_order=MarketOrderSpec(
                            instrument=StockSpecs("AMD"),
                            tif="DAY",
                            quantity=1,
                            direction=Side.BUY
                        )
                    ),
                ],
                take_profit=None,
            )
    def test_bracket_order_intent_raises_if_take_profit_direction_same_as_entry(self):
        with pytest.raises(ValueError):
            BracketOrderSpec(
                entry=LimitOrderSpec(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=None,
                take_profit=[
                    LimitOrderSpec(
                        quantity=1,
                        direction=Side.BUY,
                        price=100.0
                    )
                ],
            )
    def test_bracket_order_intent_raises_if_stop_loss_quantity_greater_than_entry(self):
        with pytest.raises(ValueError):
            BracketOrderSpec(
                entry=LimitOrderSpec(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=[
                    StopMarketOrderSpec(
                        trigger_price=100.0,
                        triggered_order=MarketOrderSpec(
                            instrument=StockSpecs("AMD"),
                            tif="DAY",
                            quantity=1,
                            direction=Side.SELL
                        )
                    ),
                    StopMarketOrderSpec(
                        trigger_price=100.0,
                        triggered_order=MarketOrderSpec(
                            instrument=StockSpecs("AMD"),
                            tif="DAY",
                            quantity=1,
                            direction=Side.SELL
                        )
                    )
                ],
                take_profit=None,
            )
    def test_bracket_order_intent_raises_if_take_profit_quantity_greater_than_entry(self):
        with pytest.raises(ValueError):
            BracketOrderSpec(
                entry=LimitOrderSpec(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=[
                    StopMarketOrderSpec(
                        trigger_price=100.0,
                        triggered_order=MarketOrderSpec(
                            instrument=StockSpecs("AMD"),
                            tif="DAY",
                            quantity=2,
                            direction=Side.SELL
                        )
                    ),
                ],
                take_profit=[
                    LimitOrderSpec(
                        quantity=1,
                        direction=Side.SELL,
                        price=100.0
                    ),
                    LimitOrderSpec(
                        quantity=1,
                        direction=Side.SELL,
                        price=100.0
                    )
                ],
            )
    def test_bracket_order_intent_valid_case(self):
        BracketOrderSpec(
            entry=LimitOrderSpec(
                quantity=2,
                direction=Side.BUY,
                price=100.0
            ),
            stop_loss=None,
            take_profit=[
                LimitOrderSpec(
                    quantity=1,
                    direction=Side.SELL,
                    price=100.0
                ),
                LimitOrderSpec(
                    quantity=1,
                    direction=Side.SELL,
                    price=100.0
                )
            ],
        )