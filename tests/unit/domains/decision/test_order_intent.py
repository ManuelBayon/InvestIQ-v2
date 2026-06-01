import pytest
from math import nan
from investiq.domain.order_intents import (
    Side,
    MarketOrderIntent,
    LimitOrderIntent,
    StopMarketOrderIntent,
    BracketOrderIntent
)

class TestMarketOrderIntent:
    def test_market_order_intent_raises_if_quantity_not_finite(self):
        with pytest.raises(ValueError):
            MarketOrderIntent(
                quantity=nan,
                direction=Side.BUY
            )
    def test_market_order_intent_raises_if_quantity_is_null(self):
        with pytest.raises(ValueError):
            MarketOrderIntent(
                quantity=0,
                direction=Side.BUY
            )
    def test_market_order_intent_raises_if_quantity_is_negative(self):
        with pytest.raises(ValueError):
            MarketOrderIntent(
                quantity=-1,
                direction=Side.BUY
            )
    def test_market_order_intent_valid_case(self):
        MarketOrderIntent(
            quantity=1,
            direction=Side.BUY
        )

class TestLimitOrderIntent:
    def test_limit_order_intent_raises_if_quantity_not_finite(self):
        with pytest.raises(ValueError):
            LimitOrderIntent(
                quantity=nan,
                direction=Side.BUY,
                price=100.0
            )
    def test_limit_order_intent_raises_if_quantity_is_null(self):
        with pytest.raises(ValueError):
            LimitOrderIntent(
                quantity=0,
                direction=Side.BUY,
                price=100.0
            )
    def test_limit_order_intent_raises_if_quantity_is_negative(self):
        with pytest.raises(ValueError):
            LimitOrderIntent(
                quantity=-1,
                direction=Side.BUY,
                price=100.0
            )
    def test_limit_order_intent_raises_if_price_not_finite(self):
        with pytest.raises(ValueError):
            LimitOrderIntent(
                quantity=1,
                direction=Side.BUY,
                price=nan
            )
    def test_limit_order_intent_raises_if_price_is_null(self):
        with pytest.raises(ValueError):
            LimitOrderIntent(
                quantity=1,
                direction=Side.BUY,
                price=0
            )
    def test_limit_order_intent_raises_if_price_is_negative(self):
        with pytest.raises(ValueError):
            LimitOrderIntent(
                quantity=1,
                direction=Side.BUY,
                price=-1
            )
    def test_limit_order_intent_valid_case(self):
        LimitOrderIntent(
            quantity=1,
            direction=Side.BUY,
            price=100.0
        )

class TestStopMarketOrderIntent:
    def test_stop_market_order_intent_raises_if_trigger_price_not_finite(self):
        with pytest.raises(ValueError):
            StopMarketOrderIntent(
                trigger_price=nan,
                triggered_order= MarketOrderIntent(
                    quantity=1,
                    direction=Side.BUY
                )
            )
    def test_stop_market_order_intent_raises_if_trigger_price_is_null(self):
        with pytest.raises(ValueError):
            StopMarketOrderIntent(
                trigger_price=0,
                triggered_order= MarketOrderIntent(
                    quantity=1,
                    direction=Side.BUY
                )
            )
    def test_stop_market_order_intent_raises_if_trigger_price_is_negative(self):
        with pytest.raises(ValueError):
            StopMarketOrderIntent(
                trigger_price=-1,
                triggered_order= MarketOrderIntent(
                    quantity=1,
                    direction=Side.BUY
                )
            )
    def test_stop_market_order_intent_valid_case(self):
        StopMarketOrderIntent(
            trigger_price=100.0,
            triggered_order=MarketOrderIntent(
                quantity=1,
                direction=Side.BUY
            )
        )

class TestBracketOrderIntent:
    def test_bracket_order_intent_raises_if_no_target_profit_and_no_stop_loss(self):
        with pytest.raises(ValueError):
            BracketOrderIntent(
                entry=LimitOrderIntent(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=None,
                take_profit=None,
            )
    def test_bracket_order_intent_raises_if_stop_loss_direction_and_entry_are_same(self):
        with pytest.raises(ValueError):
            BracketOrderIntent(
                entry=LimitOrderIntent(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=[
                    StopMarketOrderIntent(
                        trigger_price=100.0,
                        triggered_order=MarketOrderIntent(
                            quantity=1,
                            direction=Side.BUY
                        )
                    ),
                ],
                take_profit=None,
            )
    def test_bracket_order_intent_raises_if_take_profit_direction_same_as_entry(self):
        with pytest.raises(ValueError):
            BracketOrderIntent(
                entry=LimitOrderIntent(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=None,
                take_profit=[
                    LimitOrderIntent(
                        quantity=1,
                        direction=Side.BUY,
                        price=100.0
                    )
                ],
            )
    def test_bracket_order_intent_raises_if_stop_loss_quantity_greater_than_entry(self):
        with pytest.raises(ValueError):
            BracketOrderIntent(
                entry=LimitOrderIntent(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=[
                    StopMarketOrderIntent(
                        trigger_price=100.0,
                        triggered_order=MarketOrderIntent(
                            quantity=1,
                            direction=Side.SELL
                        )
                    ),
                    StopMarketOrderIntent(
                        trigger_price=100.0,
                        triggered_order=MarketOrderIntent(
                            quantity=1,
                            direction=Side.SELL
                        )
                    )
                ],
                take_profit=None,
            )
    def test_bracket_order_intent_raises_if_take_profit_quantity_greater_than_entry(self):
        with pytest.raises(ValueError):
            BracketOrderIntent(
                entry=LimitOrderIntent(
                    quantity=1,
                    direction=Side.BUY,
                    price=100.0
                ),
                stop_loss=[
                    StopMarketOrderIntent(
                        trigger_price=100.0,
                        triggered_order=MarketOrderIntent(
                            quantity=2,
                            direction=Side.SELL
                        )
                    ),
                ],
                take_profit=[
                    LimitOrderIntent(
                        quantity=1,
                        direction=Side.SELL,
                        price=100.0
                    ),
                    LimitOrderIntent(
                        quantity=1,
                        direction=Side.SELL,
                        price=100.0
                    )
                ],
            )
    def test_bracket_order_intent_valid_case(self):
        BracketOrderIntent(
            entry=LimitOrderIntent(
                quantity=2,
                direction=Side.BUY,
                price=100.0
            ),
            stop_loss=None,
            take_profit=[
                LimitOrderIntent(
                    quantity=1,
                    direction=Side.SELL,
                    price=100.0
                ),
                LimitOrderIntent(
                    quantity=1,
                    direction=Side.SELL,
                    price=100.0
                )
            ],
        )