from queue import LifoQueue

CHAR_PAIR_LOOKUP = {
    "}": "{",
    ")": "(",
    ">": "<",
    "]": "["
}


def find_corrupted_character(syntax_line):
    character_queue = LifoQueue()
    for char in syntax_line:
        if char in CHAR_PAIR_LOOKUP.keys():
            # Character is a closing character: check if it matches previous char in queue
            last_char = character_queue.get()
            if not last_char == CHAR_PAIR_LOOKUP[char]:
                return char
        else:
            # Character is an opening character: add it to the queue
            character_queue.put(char)
    return None


SCORE_LOOKUP = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


def find_syntax_error_score(lines):
    corrupted_characters = filter(None, [find_corrupted_character(l) for l in lines])

    return sum([
        SCORE_LOOKUP[c]
        for c in corrupted_characters
    ])


def read_nav_subsystem_lines(file):
    return [l.strip() for l in file.readlines()]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        lines = read_nav_subsystem_lines(f)
        score = find_syntax_error_score(lines)
        print(f"Syntax error score: {score}")