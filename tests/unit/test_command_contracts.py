"""Contract checks independent of the legacy runtime and broker SDK."""

import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
from decimal import Decimal

from investiq.contracts.bracket_spec import BracketSpec
from investiq.contracts.command_envelope import CommandEnvelope
from investiq.contracts.command_id import CommandId
from investiq.contracts.commands.cancel_order import CancelOrder
from investiq.contracts.commands.modify_order import ModifyOrder
from investiq.contracts.commands.submit_bracket import SubmitBracket
from investiq.contracts.commands.submit_order import SubmitOrder
from investiq.contracts.event import Event
from investiq.contracts.event_envelope import EventEnvelope
from investiq.contracts.event_ref import EventRef
from investiq.contracts.execution_spec import Limit, Market, StopMarket
from investiq.contracts.inputs.market_trade_received import MarketTradeReceived
from investiq.contracts.order_id import OrderId
from investiq.contracts.order_spec import OrderSpec
from investiq.contracts.recorded_command import RecordedCommand
from investiq.contracts.side import Side
from investiq.contracts.time_in_force import TimeInForce


class CommandContractTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 7, tzinfo=timezone.utc)
        self.ref = EventRef("run", 1)
        self.cid = CommandId("command")
        self.oid = OrderId("entry")
        self.entry = OrderSpec("TEST", Side.BUY, Decimal("10"), Market(), TimeInForce.DAY)
        self.tp = replace(self.entry, side=Side.SELL, execution=Limit(Decimal("110")))
        self.sl = replace(self.entry, side=Side.SELL, execution=StopMarket(Decimal("90")))

    def test_shared_event_reference_and_command_context(self):
        event = Event(EventEnvelope(self.ref, self.now),
                      MarketTradeReceived("TEST", self.now, Decimal("100"), Decimal("1")))
        commands = [SubmitOrder(self.cid, self.oid, self.entry),
                    SubmitBracket(self.cid, self.oid, OrderId("tp"), OrderId("sl"),
                                  BracketSpec(self.entry, self.tp, self.sl)),
                    ModifyOrder(self.cid, self.oid, total_quantity=Decimal("8")),
                    CancelOrder(self.cid, self.oid)]
        for command in commands:
            with self.subTest(command=type(command).__name__):
                recorded = RecordedCommand(CommandEnvelope(event.envelope.event_ref, self.now), command)
                self.assertIs(recorded.command, command)
                self.assertEqual(recorded.envelope.causation_ref, self.ref)

    def test_reference_validation(self):
        for sequence in (True, 0, -1, 1.5):
            with self.subTest(sequence=sequence), self.assertRaises((TypeError, ValueError)):
                EventRef("run", sequence)
        for cls in (CommandId, OrderId):
            with self.assertRaises(ValueError):
                cls("")

    def test_envelope_validation(self):
        for cls, field in ((EventEnvelope, "received_at_utc"),
                           (CommandEnvelope, "created_at_utc")):
            with self.subTest(cls=cls), self.assertRaises(ValueError):
                cls(self.ref, self.now.replace(tzinfo=None))
            with self.assertRaises(TypeError):
                cls("raw-reference", self.now)

    def test_bracket_exit_identity_presence(self):
        for tp, sl in ((self.tp, None), (None, self.sl), (self.tp, self.sl)):
            spec = BracketSpec(self.entry, tp, sl)
            command = SubmitBracket(self.cid, self.oid,
                                    OrderId("tp") if tp else None,
                                    OrderId("sl") if sl else None, spec)
            for field in ("take_profit_id", "stop_loss_id"):
                wrong = None if getattr(command, field) is not None else OrderId("extra")
                with self.subTest(field=field, spec=spec), self.assertRaises(ValueError):
                    replace(command, **{field: wrong})

    def test_bracket_ids_must_be_distinct(self):
        spec = BracketSpec(self.entry, self.tp, self.sl)
        for ids in ((self.oid, self.oid, OrderId("sl")),
                    (self.oid, OrderId("tp"), self.oid),
                    (self.oid, OrderId("exit"), OrderId("exit"))):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                SubmitBracket(self.cid, *ids, spec)

    def test_modification_requires_an_explicit_change(self):
        with self.assertRaises(ValueError):
            ModifyOrder(self.cid, self.oid)
        for quantity in (Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 8.0):
            with self.subTest(quantity=quantity), self.assertRaises((TypeError, ValueError)):
                ModifyOrder(self.cid, self.oid, total_quantity=quantity)
        with self.assertRaises(TypeError):
            ModifyOrder(self.cid, self.oid, new_execution=Market())
        for execution in (Limit(Decimal("112")), StopMarket(Decimal("92"))):
            ModifyOrder(self.cid, self.oid, new_execution=execution)
            ModifyOrder(self.cid, self.oid, Decimal("8"), execution)

    def test_containers_reject_unsupported_content(self):
        with self.assertRaises(TypeError):
            Event(EventEnvelope(self.ref, self.now), object())
        with self.assertRaises(TypeError):
            RecordedCommand(CommandEnvelope(self.ref, self.now), object())
        with self.assertRaises(TypeError):
            CancelOrder("raw-command", self.oid)

    def test_immutability(self):
        command = CancelOrder(self.cid, self.oid)
        with self.assertRaises(FrozenInstanceError):
            command.order_id = OrderId("other")


if __name__ == "__main__":
    unittest.main()
