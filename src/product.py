from dataclasses import dataclass


@dataclass
class Product:
    id: int
    description: str
    price: float

    def update_info(self, description, price):
        self.description = description
        self.price = price
