from src.countries import Country
from src.shipping import calculate_shipping, get_region_by_country


def print_shipping_costs(country, order_total):
    region = get_region_by_country(country)
    shipping = calculate_shipping(region, order_total)
    print(f'Shipping cost to {country} for order total £{order_total} is £{shipping}')


if __name__ == '__main__':
    print_shipping_costs(Country.UNITED_KINGDOM.value, 99.99)
    print_shipping_costs(Country.UNITED_KINGDOM.value, 100.00)
    print_shipping_costs(Country.FRANCE.value, 99.99)
    print_shipping_costs(Country.FRANCE.value, 100.00)
    print_shipping_costs(Country.ALBANIA.value, 99.99)
    print_shipping_costs(Country.ALBANIA.value, 100.00)
