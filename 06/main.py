from operator import add
import functools


def simulate_fish_population(days, fish_list):
    lanternfish = [f for f in fish_list]
    for _ in range(0, days):
        next_day_counts = [0] * 9
        for i, count in enumerate(lanternfish):
            if i == 0:
                # Add new lanternfish
                next_day_counts[8] += count
                # repeat existing lanternfish
                next_day_counts[6] += count
            else:
                next_day_counts[i - 1] += count
        lanternfish = next_day_counts

    return functools.reduce(add, lanternfish)


def parse_lanternfish(file):
    """
    returns a list where the index represents the number of days a fish
    has until reproduction and the value at each index represents the
    number of fish that share remaining days #
    """
    fish_counts = [0] * 9
    for n in file.read().strip().split(","):
        fish_counts[int(n)] += 1

    return fish_counts


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        lanternfish = parse_lanternfish(f)
        print(f"Fish after 80 days: {simulate_fish_population(80, lanternfish)}")
        print(f"Fish after 256 days: {simulate_fish_population(256,lanternfish)}")