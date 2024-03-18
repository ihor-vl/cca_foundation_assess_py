from dataclasses import dataclass

import pytest

from src.product import Product


@dataclass
class InitialProductData:
    id: int
    description: str
    price: float


@dataclass
class UpdatedProductData:
    description: str
    price: float


@pytest.mark.parametrize(
    "initial_product_data,updated_product_data,expected_product",
    [
        pytest.param(
            InitialProductData(1, "dummy-description", 10.0),
            UpdatedProductData("new-dummy-description", 10.0),
            Product(1, "new-dummy-description", 10.0),
            id="Update_product_description"
        ),
        pytest.param(
            InitialProductData(1, "dummy-description", 10.0),
            UpdatedProductData("dummy-dummy", 12.0),
            Product(1, "dummy-dummy", 12.0),
            id="Update_product_price"
        ),
        pytest.param(
            InitialProductData(1, "dummy-description", 10.0),
            UpdatedProductData("new-dummy-dummy", 12.0),
            Product(1, "new-dummy-dummy", 12.0),
            id="Update_product_price_and_description"
        ),
    ],
)
def test_update_product_info(initial_product_data, updated_product_data, expected_product):
    product = Product(
       initial_product_data.id,
       initial_product_data.description,
       initial_product_data.price
    )
    product.update_info(updated_product_data.description, updated_product_data.price)
    assert product.id == expected_product.id
    assert product.description == expected_product.description
    assert product.price == expected_product.price
