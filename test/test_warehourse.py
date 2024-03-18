from dataclasses import dataclass

import pytest

from src.product import Product
from src.warehouse import Entry, Warehouse


def compare_catalogues(catalogue_under_test, expected_catalogue):

    assert len(catalogue_under_test) == len(expected_catalogue)
    for entry in catalogue_under_test:
        expected_item = next(
            (expected_entry for expected_entry in expected_catalogue
             if expected_entry.product.id == entry.product.id),
            False
        )
        assert expected_item
        assert entry.stock == expected_item.stock
        assert entry.product.id == expected_item.product.id
        assert entry.product.description == expected_item.product.description
        assert entry.product.price == expected_item.product.price



@dataclass
class ReceiveStockInput:
    product_id: int
    product_description: str
    product_price: float
    quantity: int


@pytest.mark.parametrize(
    "receive_stock_input,warehouse_catalogue,expected_warehouse_catalogue",
    [
        pytest.param(
            ReceiveStockInput(1, "dummy-description", 10.0, 10),
            [],
            [Entry(Product(1, "dummy-description", 10.0), 10)],
            id="Receiving stock for the first time"
        ),
        pytest.param(
            ReceiveStockInput(1, "dummy-description", 10.0, 10),
            [Entry(Product(1, "dummy-description", 10.0), 10)],
            [Entry(Product(1, "dummy-description", 10.0), 20)],
            id="Receiving stock for the second time"
        ),
        pytest.param(
            ReceiveStockInput(2, "another-dummy-description", 12.0, 3),
            [Entry(Product(1, "dummy-description", 10.0), 10)],
            [
                Entry(Product(1, "dummy-description", 10.0), 10),
                Entry(Product(2, "another-dummy-description", 12.0), 3),
            ],
            id="Receiving a new stock for the first time for non-empty catalogue"
        ),
    ],
)
def test_receive_stock(receive_stock_input, warehouse_catalogue, expected_warehouse_catalogue):
    warehouse = Warehouse(catalogue=warehouse_catalogue)
    warehouse.receive_stock(
        receive_stock_input.product_id,
        receive_stock_input.product_description,
        receive_stock_input.product_price,
        receive_stock_input.quantity
    )

    compare_catalogues(warehouse.catalogue, expected_warehouse_catalogue)
