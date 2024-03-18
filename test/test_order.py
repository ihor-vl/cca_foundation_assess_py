import pytest

from src.countries import Country
from src.order import Order, Item
from src.product import Product
from src.warehouse import Warehouse, Entry
from src.address import Address


def compare_items(items_under_test, expected_items):

    assert len(items_under_test) == len(expected_items)
    for item in items_under_test:
        expected_item = next(
            (expected_item for expected_item in expected_items
             if expected_item.product.id == item.product.id),
            False
        )
        assert expected_item
        assert item.quantity == expected_item.quantity
        assert item.product.id == expected_item.product.id
        assert item.product.description == expected_item.product.description
        assert item.product.price == expected_item.product.price


@pytest.mark.parametrize(
    "order, product_ids, quantities, warehouse, expected_items",
    [
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street", 
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ), 
                items=[]
            ),
            [1],
            [10],
            Warehouse(catalogue=[Entry(Product(1, "dummy-description", 10.0), 10)]),
            [Item(Product(1, "dummy-description", 10.0), 10)],
            id="Add item in stock to the order"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ),
                items=[]
            ),
            [1, 2],
            [10, 7],
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 10),
                Entry(Product(2, "another-dummy-description", 12.0), 13),
            ]),
            [
                Item(Product(1, "dummy-description", 10.0), 10),
                Item(Product(2, "another-dummy-description", 12.0), 7),
            ],
            id="Add 2 items in stock to the order"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ),
                items=[]
            ),
            [1],
            [10],
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 1),
            ]),
            [],
            id="Add item out of stock to the order"
        ),
    ],
    
)
def test_add_item(order, product_ids, quantities, warehouse, expected_items):
    for product_id, quantity in zip(product_ids, quantities):
        order.add_item(product_id, quantity, warehouse)
    compare_items(order.items, expected_items)


@pytest.mark.parametrize(
    "order, expected_total",
    [
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 10),
                    Item(Product(2, "another-dummy-description", 12.0), 7),
                ],
                region_getter=lambda country: "EU"
            ),
            188.99,
            id="Calculate total for 2 items in Europe over 100.00"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 5),
                ],
                region_getter=lambda country: "EU"
            ),
            58.99,
            id="Calculate total for 1 item in Europe under 100.00"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UNITED_KINGDOM.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 10),
                ],
                region_getter=lambda country: "UK"
            ),
            104.99,
            id="Calculate total for 1 item in UK below 120.00"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UNITED_KINGDOM.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 10),
                    Item(Product(2, "dummy-description-2", 2.0), 17),
                    Item(Product(3, "dummy-description-3", 12.0), 2),
                ],
                region_getter=lambda country: "UK"
            ),
            158.00,
            id="Calculate total for 3 items in UK over 120.00"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.ALBANIA.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 18),
                ],
                region_getter=lambda country: "OTHER"
            ),
            189.99,
            id="Calculate total for 1 item in OTHER below 200.00"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.ALBANIA.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 18),
                    Item(Product(2, "anoter-dummy-description", 20.0), 3),
                ],
                region_getter=lambda country: "OTHER"
            ),
            245.99,
            id="Calculate total for 2 items in OTHER over 200.00"
        ),
    ],
)
def test_total(order, expected_total):
    assert order.total() == expected_total


@pytest.mark.parametrize(
    "order, warehouse, warehouse_after_confirmation",
    [
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 10),
                    Item(Product(2, "another-dummy-description", 12.0), 7),
                ]
            ),
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 10),
                Entry(Product(2, "another-dummy-description", 12.0), 13),
            ]),
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 0),
                Entry(Product(2, "another-dummy-description", 12.0), 6),
            ]),
            id="Confirm order with 2 items"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ),
                items=[
                    Item(Product(1, "dummy-description", 10.0), 8),
                ]
            ),
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 10),
            ]),
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 2),
            ]),
            id="Confirm order with 1 item"
        ),
        pytest.param(
            Order(
                shipping_address=Address(
                    "dummy-house", "dummy-street",
                    "dummy-city", "dummy-zip", Country.UKRAINE.value
                ),
                items=[]
            ),
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 12),
            ]),
            Warehouse(catalogue=[
                Entry(Product(1, "dummy-description", 10.0), 12),
            ]),
            id="Confirm order with no items"
        ),
    ]
)
def test_confirm(order, warehouse, warehouse_after_confirmation):
    order.confirm(warehouse)
    for item in order.items:
        assert (
            warehouse.check_stock(item.product.id)
            == warehouse_after_confirmation.check_stock(item.product.id)
        )
