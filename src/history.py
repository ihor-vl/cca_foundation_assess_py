from dataclasses import dataclass
from order import Order


@dataclass
class SalesHistory:
    orders: list[Order]

    def add_order(self, order: Order) -> None:
        self.orders.append(order)
