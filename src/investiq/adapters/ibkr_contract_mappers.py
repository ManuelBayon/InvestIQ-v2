from ib_insync import Stock, Future

from investiq.domain.instruments import StockSpecs, FutureSpecs


def map_stock_specs_to_ib_contract(specs: StockSpecs) -> Stock:
    return Stock(
        symbol=specs.symbol,
        exchange=specs.exchange,
        currency=specs.currency
    )


def map_future_specs_to_ib_contract(specs: FutureSpecs) -> Future:
    return Future(
        symbol=specs.symbol,
        localSymbol=specs.local_symbol,
        exchange=specs.exchange,
        currency=specs.currency,
    )