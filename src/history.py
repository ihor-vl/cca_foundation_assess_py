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
