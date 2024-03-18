from dataclasses import dataclass

from src.countries import Country


@dataclass
class Address:
    house: str
    street: str
    city: str
    postcode: str
    country: Country

    def matches(self, house, street, city, postcode, country) -> bool:
        return (
            self.house == house and
            self.street == street and
            self.city == city and
            self.postcode == postcode and
            self.country == country
        )
