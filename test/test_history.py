import pytest

from src.address import Address
from src.countries import Country
from src.history import SalesHistory
from src.order import Order, Item
from src.product import Product
from test.utils import compare_history


@pytest.mark.parametrize(
    "history, orders, history_orders_after_confirmation",
    [
        pytest.param(
            SalesHistory(orders=[]),
            [
                Order(
                    shipping_address=Address(
                        "dummy-house", "dummy-street",
                        "dummy-city", "dummy-zip", Country.UKRAINE.value
                    ),
                    items=[
                        Item(Product(1, "dummy-description", 10.0), 10),
                        Item(Product(2, "another-dummy-description", 12.0), 7),
                    ],
                ),
            ],
            [
                Order(
                    shipping_address=Address(
                        "dummy-house", "dummy-street",
                        "dummy-city", "dummy-zip", Country.UKRAINE.value
                    ),
                    items=[
                        Item(Product(1, "dummy-description", 10.0), 10),
                        Item(Product(2, "another-dummy-description", 12.0), 7),
                    ],
                ),
            ],
            id="Add one new order"
        ),
        pytest.param(
            SalesHistory(orders=[
                Order(
                    shipping_address=Address(
                        "dummy-house", "dummy-street",
                        "dummy-city", "dummy-zip", Country.UNITED_KINGDOM.value
                    ),
                    items=[
                        Item(Product(1, "dummy-description-1", 12.0), 35),
                        Item(Product(2, "another-dummy-description-1", 15.0), 4),
                    ],
                ),
            ]),
            [
                Order(
                    shipping_address=Address(
                        "dummy-house", "dummy-street",
                        "dummy-city", "dummy-zip", Country.UKRAINE.value
                    ),
                    items=[
                        Item(Product(1, "dummy-description", 10.0), 10),
                        Item(Product(2, "another-dummy-description", 12.0), 7),
                    ],
                ),
            ],
            [
                Order(
                    shipping_address=Address(
                        "dummy-house", "dummy-street",
                        "dummy-city", "dummy-zip", Country.UNITED_KINGDOM.value
                    ),
                    items=[
                        Item(Product(1, "dummy-description-1", 12.0), 35),
                        Item(Product(2, "another-dummy-description-1", 15.0), 4),
                    ],
                ),
                Order(
                    shipping_address=Address(
                        "dummy-house", "dummy-street",
                        "dummy-city", "dummy-zip", Country.UKRAINE.value
                    ),
                    items=[
                        Item(Product(1, "dummy-description", 10.0), 10),
                        Item(Product(2, "another-dummy-description", 12.0), 7),
                    ],
                ),
            ],
            id="Add one new order to the existing history"
        ),
    ]
)
def test_add_order(history, orders, history_orders_after_confirmation):
    for order in orders:
        history.add_order(order)

    compare_history(history.orders, history_orders_after_confirmation)
