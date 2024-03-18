from dataclasses import dataclass
from typing import Callable

from address import Address
from product import Product
from src.shipping import get_region_by_country, calculate_shipping
from src.warehouse import Warehouse


@dataclass
class Item:
    product: Product
    quantity: int


@dataclass
class Order:
    shipping_address: Address
    items: list[Item]
    region_getter: Callable = get_region_by_country

    def add_item(self, product_id: int, quantity: int, warehouse: Warehouse) -> None:
        if warehouse.check_stock(product_id) < quantity:
            print('Not enough stock')
            return
        product = warehouse.get_product(product_id)
        if product:
            self.items.append(Item(product, quantity))

    def total(self) -> float:
        total = 0.0
        for item in self.items:
            total += item.product.price * item.quantity
        region = self.get_region()
        shipping_cost = calculate_shipping(region, total)
        return total + shipping_cost

    def adjust(self, warehouse) -> None:
        for item in self.items:
            warehouse.adjust_stock(item.product.id, item.quantity)

    def log_history(self, history) -> None:
        history.add_order(self)

    def confirm(self, warehouse, history) -> None:
        self.adjust(warehouse)
        self.log_history(history)

    def get_region(self):
        return self.region_getter(self.shipping_address.country)
