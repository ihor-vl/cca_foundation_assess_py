from dataclasses import dataclass
from order import Order


@dataclass
class SalesHistory:
    orders: list[Order]

    def add_order(self, order: Order) -> None:
        self.orders.append(order)

    def list_orders_by_product(self, product_id: int) -> list[Order]:
        return [
            order for order in self.orders
            if any(item.product.id == product_id for item in order.items)
        ]

    def list_orders_by_address(self, house, street, city, postcode, country) -> list[Order]:
        return [
            order for order in self.orders
            if order.shipping_address.house == house
            and order.shipping_address.street == street
            and order.shipping_address.city == city
            and order.shipping_address.postcode == postcode
            and order.shipping_address.country == country
        ]
