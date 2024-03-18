import pytest

from src.history import SalesHistory


def compare_history(orders, history_orders_after_confirmation):
    assert len(orders) == len(history_orders_after_confirmation)
    for order in orders:
        expected_order = next(
            (expected_order for expected_order in history_orders_after_confirmation
             if expected_order.id == order.id),
            False
        )
        assert expected_order
        assert order.shipping_address == expected_order.shipping_address
        assert order.items == expected_order.items


@pytest.mark.parametrize(
    "orders, history_orders_after_confirmation",
    []
)
@pytest.mark.skip(reason="Not ready yet")
def test_add_order(orders, history_orders_after_confirmation):
    history = SalesHistory(orders=[])
    history.add_order(orders)

    compare_history(history.orders, history_orders_after_confirmation)
