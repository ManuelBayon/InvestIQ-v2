from ib_insync import OrderStatus

def _make_ibkr_order_status_fixture(
        order_id: int,
        status: str,
        filled: float,
        remaining: float,
        avg_fill_price: float,
        perm_id: int,
        parent_id: int,
        last_fill_price: float,
        client_id: int,
        why_held: str,
        mkt_cap_price: float,
) -> OrderStatus:
    return OrderStatus(
        orderId=order_id,
        status=status,
        filled=filled,
        remaining=remaining,
        avgFillPrice=avg_fill_price,
        permId=perm_id,
        parentId=parent_id,
        lastFillPrice=last_fill_price,
        clientId=client_id,
        whyHeld=why_held,
        mktCapPrice=mkt_cap_price,
    )

def make_presubmitted_order_status(
        order_id: int = 277,
        perm_id: int = 2005721994,
        quantity: float = 1.0,
) -> OrderStatus:
    return _make_ibkr_order_status_fixture(
        order_id=order_id,
        status=OrderStatus.PreSubmitted,
        filled=0.0,
        remaining=quantity,
        avg_fill_price=0.0,
        perm_id=perm_id,
        parent_id=0,
        last_fill_price=0.0,
        client_id=1,
        why_held='',
        mkt_cap_price=0.0,
    )