import subprocess


def compare_golden_master(stdout_lines, expected_results):
    assert len(stdout_lines) == len(expected_results)
    for line, expected in zip(stdout_lines, expected_results):
        assert line == expected


def test_shipping_costs_match_expected_results():
    with open('test/existing_shipping_cost_results.txt') as file:
        expected_shipping_costs = file.read().splitlines()

    process = subprocess.run(['python', 'main.py'], stdout=subprocess.PIPE, text=True)
    stdout_lines = process.stdout.splitlines()

    compare_golden_master(stdout_lines, expected_shipping_costs)
