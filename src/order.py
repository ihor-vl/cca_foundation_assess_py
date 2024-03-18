from dataclasses import dataclass

from address import Address
from product import Product
from src.warehouse import Warehouse


@dataclass
class Item:
    product: Product
    quantity: int


@dataclass
class Order:
    shipping_address: Address
    items: list[Item]

    def add_item(self, product_id: int, quantity: int, warehouse: Warehouse) -> None:
        if warehouse.check_stock(product_id) < quantity:
            print('Not enough stock')
            return
        product = warehouse.get_product(product_id)
        if product:
            self.items.append(Item(product, quantity))

    def total(self) -> float:
        pass

    def confirm(self) -> None:
        pass
