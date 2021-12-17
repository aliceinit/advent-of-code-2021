from datetime import datetime


class PolymerElement:
    def __init__(self, letter):
        self.letter = letter
        self.next = None

    def __repr__(self):
        polymer = "" + self.letter
        next = self.next
        while next:
            polymer += next.letter
            next = next.next
        return polymer

    def get_letter_counts(self):
        counts = {}
        node = self
        while node is not None:
            if not counts.get(node.letter):
                counts[node.letter] = 1
            else:
                counts[node.letter] += 1
            node = node.next
        return counts

    def drop_final_character(self):
        previous = self
        next = self.next
        while next.next is not None:
            previous = next
            next = next.next
        previous.next = None


class Polymer(PolymerElement):
    def __init__(self, string):
        super().__init__(string[0])
        self.next = PolymerElement(string[1])
        last = self.next
        if len(string) > 2:
            for s in string[2:]:
                element = PolymerElement(s)
                last.next = element
                last = element


def insert_between(left: PolymerElement, right: PolymerElement, insert):
    """Insert one or more elements between two others"""
    previous = left
    if isinstance(insert, str):
        for letter in insert:
            next = PolymerElement(letter)
            previous.next = next
            previous = next
    elif isinstance(insert, PolymerElement):
        left.next = insert
        previous = insert
        next = insert.next
        while next is not None:
            previous = next
            next = previous.next

    previous.next = right


def expand_polymer(args):
    first_element, rules = args

    left = first_element
    right = first_element.next
    while right is not None:
        insert_between(left, right,
                       rules[f"{left.letter}{right.letter}"])
        left = right
        right = right.next
    return first_element


def expand_rules(rules, step_count):
    i = 1
    start_time = datetime.now()
    new_rules = {pair: Polymer(f"{pair[0]}{rules[pair]}{pair[1]}") for pair in rules.keys()}
    while i < step_count:
        for pair in rules.keys():
            expand_polymer((new_rules[pair], rules))
        i += 1
    t = (datetime.now() - start_time).total_seconds()
    # Drop first letter from expansions
    new_rules = {pair: new_rules[pair].next for pair in new_rules.keys()}
    # Drop final letter from expansions
    for expansion in new_rules.values():
        expansion.drop_final_character()

    print(f"Finished creating expansion of rules to depth {step_count} in {t} seconds")
    return new_rules


def find_most_and_least_common_elements(polymer, insertion_rules, step_count):
    print("Expanding rules...")
    expanded_rules = expand_rules(insertion_rules, int(step_count / 2))
    # Pre-calculate counts for expansions
    print("Calculating expansion counts...")
    expansion_counts = {pair: expansion.get_letter_counts()
                        for pair, expansion in expanded_rules.items()}

    # convert expansions to string:
    expanded_rules = {pair: str(expansion)
                      for pair, expansion in expanded_rules.items()}

    if step_count % 2 == 1:
        # Account for odd number by expanding initial polymer once
        print("Performing additional expansion for uneven step count")
        expand_polymer((polymer, insertion_rules))

    # Expand polymer to its half-way point using expanded rules:
    print("Performing final expansion...")
    expand_polymer((polymer, expanded_rules))

    # Set up for tracking counts
    letters = set()
    for pair in expanded_rules.keys():
        letters.add(pair[0])
        letters.add(pair[1])
    counts = {l: 0 for l in letters}

    print("Starting Counts...")
    # For each pair, count the left char + substitution
    left = polymer
    right = polymer.next

    while right is not None:
        counts[left.letter] += 1
        inner_count = expansion_counts[f"{left.letter}{right.letter}"]
        for letter, count in inner_count.items():
            counts[letter] += count
        left = right
        right = right.next

    # Count the very last character
    counts[left.letter] += 1

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

    return Polymer(lines[0]), rules


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        polymer, rules = parse_polymer_and_rules(f)
        polymer_part_2 = Polymer(str(polymer))
        print(polymer_part_2)

        _, most_count, _, least_count = find_most_and_least_common_elements(
            polymer, rules, 10)

        print(f"most minus least after 10 rounds: {most_count - least_count}")

        _, most_count_40, _, least_count_40 = find_most_and_least_common_elements(
            polymer_part_2, rules, 40)
        print(f"most minus least after 40 rounds: {most_count_40 - least_count_40}")
