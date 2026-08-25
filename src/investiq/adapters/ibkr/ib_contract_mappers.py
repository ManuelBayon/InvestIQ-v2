from ib_insync import Stock, Future

from investiq.domain.instrument_spec import StockSpec, FutureSpec


def map_stock_specs_to_ib_contract(spec: StockSpec) -> Stock:
    return Stock(
        symbol=spec.symbol,
        exchange=spec.exchange,
        currency=spec.currency
    )


def map_future_specs_to_ib_contract(spec: FutureSpec) -> Future:
    return Future(
        symbol=spec.symbol,
        localSymbol=spec.local_symbol,
        exchange=spec.exchange,
        currency=spec.currency,
    )