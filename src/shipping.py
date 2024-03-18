import requests as requests


SHIPPING_RATES_BY_REGION = {
    "UK": {
        "threshold": 120.0,
        "under_threshold": 4.99,
        "over_threshold": 0.0
    },
    "EU": {
        "threshold": 100.0,
        "under_threshold": 8.99,
        "over_threshold": 4.99
    },
    "OTHER": {
        "threshold": 200.0,
        "under_threshold": 9.99,
        "over_threshold": 5.99
    }
}


def get_region_by_country(country):
    url = "https://npovmrfcyzu2gu42pmqa7zce6a0zikbf.lambda-url.eu-west-2.on.aws/?country=" + country

    response = requests.get(url)
    response.raise_for_status()

    return response.json()["region"]


def calculate_shipping(region, order_total):
    shipping_rates = SHIPPING_RATES_BY_REGION[region]
    return (
        shipping_rates["under_threshold"]
        if order_total < shipping_rates["threshold"]
        else shipping_rates["over_threshold"]
    )
