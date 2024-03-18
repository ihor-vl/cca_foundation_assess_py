from dataclasses import dataclass, field

from product import Product


@dataclass
class Entry:
    product: Product
    stock: int

    @classmethod
    def init_entry(cls,
                   product_id: int,
                   product_description: str,
                   product_price: float,
                   quantity: int) -> 'Entry':
        product = Product(product_id, product_description, product_price)
        return Entry(product, quantity)

    def update_info(self,
                    product_description: str,
                    product_price: float,
                    quantity: int) -> None:
        self.product.update_info(product_description, product_price)
        self.stock += quantity


@dataclass
class Warehouse:
    catalogue: list[Entry] = field(default_factory=list)

    def receive_stock(self,
                      product_id: int,
                      product_description: str,
                      product_price: float,
                      quantity: int) -> None:

        entry = Entry.init_entry(product_id, product_description, product_price, quantity)
        entry_in_catalogue = next(
            (entry for entry in self.catalogue if entry.product.id == product_id),
            None
        )
        if entry_in_catalogue:
            entry_in_catalogue.update_info(product_description, product_price, quantity)
        else:
            self.catalogue.append(entry)

    def check_stock(self, product_id: int) -> int:
        entry = next(
            (entry for entry in self.catalogue if entry.product.id == product_id),
            None
        )
        if entry:
            return entry.stock
        return 0

    def adjust_stock(self, product_id: int, quantity: int) -> None:
        entry = next(
            (entry for entry in self.catalogue if entry.product.id == product_id),
            None
        )
        if entry:
            entry.stock -= quantity
