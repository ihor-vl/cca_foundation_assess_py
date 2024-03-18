import subprocess

import pytest

from src.shipping import calculate_shipping


def compare_golden_master(stdout_lines, expected_results):
    assert len(stdout_lines) == len(expected_results)
    for line, expected in zip(stdout_lines, expected_results):
        assert line == expected


@pytest.mark.skip(reason="No need in this test anymore, as legacy logic is changed")
def test_shipping_costs_match_expected_results():
    with open('test/existing_shipping_cost_results.txt') as file:
        expected_shipping_costs = file.read().splitlines()

    process = subprocess.run(['python', 'main.py'], stdout=subprocess.PIPE, text=True)
    stdout_lines = process.stdout.splitlines()

    compare_golden_master(stdout_lines, expected_shipping_costs)


@pytest.mark.parametrize(
    'region, order_total, expected_shipping_cost',
    [
        ('UK', 99.99, 4.99),
        ('UK', 100.00, 4.99),
        ('UK', 119.99, 4.99),
        ('UK', 120.00, 0.0),
        ('EU', 99.99, 8.99),
        ('EU', 100.00, 4.99),
        ('OTHER', 199.99, 9.99),
        ('OTHER', 200.00, 5.99),
    ]
)
def test_shipping_costs(region, order_total, expected_shipping_cost):
    shipping_cost = calculate_shipping(region, order_total)
    assert shipping_cost == expected_shipping_cost
