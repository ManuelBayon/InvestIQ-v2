import pytest
from ib_insync import Stock

from investiq.refactoring.ibkr_instruments import IBKRInstruments


def test_resolve_uses_canonical_symbol_and_accepts_contract_without_con_id():
    instruments = IBKRInstruments(
        {
            "US:MSFT": Stock("MSFT", "SMART", "USD"),
            "US:AAPL": Stock("AAPL", "SMART", "USD"),
        }
    )

    contract = instruments.resolve("US:AAPL")

    assert (contract.symbol, contract.exchange, contract.currency) == ("AAPL", "SMART", "USD")
    assert contract.conId == 0


def test_resolve_raises_key_error_for_unknown_symbol():
    instruments = IBKRInstruments({"US:AAPL": Stock("AAPL", "SMART", "USD")})

    with pytest.raises(KeyError, match="US:MSFT"):
        instruments.resolve("US:MSFT")


def test_catalog_is_isolated_from_changes_to_the_input_contract():
    contract = Stock("AAPL", "SMART", "USD")
    instruments = IBKRInstruments({"US:AAPL": contract})

    contract.exchange = "NASDAQ"

    assert instruments.resolve("US:AAPL").exchange == "SMART"


def test_catalog_is_isolated_from_changes_to_a_resolved_contract():
    instruments = IBKRInstruments({"US:AAPL": Stock("AAPL", "SMART", "USD")})

    contract = instruments.resolve("US:AAPL")
    contract.exchange = "NASDAQ"

    assert instruments.resolve("US:AAPL").exchange == "SMART"
