from datetime import datetime
from collections import deque


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


def process_insertion_step(polymer_chain, rules):
    current_element = polymer_chain
    while current_element.next is not None:
        insert = PolymerElement(rules.get(current_element.letter + current_element.next.letter))

        # Insert new element
        insert.next = current_element.next
        current_element.next = insert

        # Advance to next element
        current_element = insert.next

    return polymer_chain


def process_insertion_single_traversal(polymer, rules, step_count):
    current_element = polymer
    processed_chars = 0

    def insert_between(this, next):
        insert = PolymerElement(rules[this.letter + next.letter])
        insert.next = next
        this.next = insert

    while current_element.next is not None:
        start_time = datetime.now()
        left_anchor = current_element
        right_anchor = current_element.next
        for depth in range(step_count):

            current = left_anchor
            next = left_anchor.next
            while next != right_anchor:
                insert_between(current, next)
                current = next
                next = next.next

            # One final insert
            insert_between(current, right_anchor)
            print(f"Processed char {processed_chars} depth = {depth} in {(datetime.now() - start_time).total_seconds()}")
        current_element = right_anchor
        print(f"Processed char {processed_chars} in {(datetime.now() - start_time).total_seconds()}")
        processed_chars += 1

    return polymer


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

    first_element = PolymerElement(lines[0][0])
    last_element = first_element
    for char in lines[0][1:]:
        next_element = PolymerElement(char)
        last_element.next = next_element
        last_element = next_element
    return first_element, rules


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        polymer, rules = parse_polymer_and_rules(f)
        process_polymer_insertions(polymer, rules, 10)
        _, most_count, _, least_count = find_most_and_least_common_elements(str(polymer))
        print(f"most minus least after 10 rounds: {most_count - least_count}")

        process_insertion_single_traversal(polymer, rules, 40)
        _, most_count_40, _, least_count_40 = find_most_and_least_common_elements(str(polymer))
        print(f"most minus least after 40 rounds: {most_count_40 - least_count_40}")
