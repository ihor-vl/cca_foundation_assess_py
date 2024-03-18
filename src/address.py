from dataclasses import dataclass

from src.countries import Country


@dataclass
class Address:
    house: str
    street: str
    city: str
    postcode: str
    country: Country
