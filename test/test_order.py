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
