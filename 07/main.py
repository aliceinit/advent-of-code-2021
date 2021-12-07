from operator import add
import functools


def calculate_min_fuel_to_align(positions):
    median = sorted(positions)[int(len(positions) / 2)]
    return functools.reduce(add, [abs(median - p) for p in positions])


def parse_positions(file):
    return [int(n) for n in file.read().strip().split(",")]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        positions = parse_positions(f)
        print(f"Min fuel needed = {calculate_min_fuel_to_align(positions)}")
