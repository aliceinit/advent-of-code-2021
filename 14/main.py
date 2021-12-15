def process_insertion_step(polymer, rules):
    result = ""
    for i in range(len(polymer) - 1):
        c1 = polymer[i]
        c2 = polymer[i + 1]
        insert = rules.get(f"{c1}{c2}")

        result = result + c1 + insert
    return result + polymer[-1]


def process_polymer_insertions(polymer, rules, step_count):
    for i in range(step_count):
        polymer = process_insertion_step(polymer, rules)
    return polymer


def find_most_and_least_common_elements(polymer):
    counts = {}
    for char in polymer:
        if not counts.get(char):
            counts[char] = 1
        else:
            counts[char] += 1

    sorted_counts = sorted([(k, v) for k, v in counts.items()],
                           key=lambda x: x[1])
    most = sorted_counts[-1]
    least = sorted_counts[0]

    return most[0], most[1], least[0], least[1]


def parse_polymer_and_rules(file):
    lines = [line.strip() for line in file.readlines()]
    rules = {}
    for line in lines[2:]:
        pair, result = line.split(" -> ")
        rules[pair] = result
    return lines[0], rules


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        polymer, rules = parse_polymer_and_rules(f)
        result_after_10 = process_polymer_insertions(polymer, rules, 10)
        _, most_count, _, least_count = find_most_and_least_common_elements(result_after_10)
        print(f"most minus least after 10 rounds: {most_count - least_count}")
