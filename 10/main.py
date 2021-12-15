from queue import LifoQueue

CLOSE_TO_OPEN_CHAR = {
    "}": "{",
    ")": "(",
    ">": "<",
    "]": "["
}
OPEN_TO_CLOSE_CHAR = {v: k for k, v in CLOSE_TO_OPEN_CHAR.items()}


def find_corrupted_character(syntax_line):
    character_queue = LifoQueue()
    for char in syntax_line:
        if char in CLOSE_TO_OPEN_CHAR.keys():
            # Character is a closing character: check if it matches previous char in queue
            last_char = character_queue.get()
            if not last_char == CLOSE_TO_OPEN_CHAR[char]:
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


def autocomplete_line(syntax_line):
    character_queue = LifoQueue()
    for char in syntax_line:
        if char in CLOSE_TO_OPEN_CHAR.keys():
            # Character is a closing character; remove char from queue
            pair = character_queue.get()
            if pair != CLOSE_TO_OPEN_CHAR[char]:
                raise RuntimeError("Cannot autocomplete corrupted line")
        else:
            # Character is an opening character: add it to the queue
            character_queue.put(char)

    # After reaching the end of the line, auto-complete remaining characters:
    remaining_chars = []

    while not character_queue.empty():
        char = character_queue.get()
        remaining_chars.append(OPEN_TO_CLOSE_CHAR[char])
    return remaining_chars


AUTOCOMPLETE_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


def get_auto_complete_line_score(line):
    remaining_chars = autocomplete_line(line)
    score = 0
    for c in remaining_chars:
        score = score * 5 + AUTOCOMPLETE_SCORES[c]
    return score


def return_middle_val(val_list):
    return val_list[int(len(val_list) / 2)]


def get_auto_complete_score(lines):
    scores = sorted([get_auto_complete_line_score(l)
                     for l in get_incomplete_lines(lines)])
    # Return middle score
    return return_middle_val(scores)


def get_incomplete_lines(lines):
    """Find and discard all lines with corrupted characters. Return remaining lines"""
    return [l for l in lines
            if find_corrupted_character(l) is None]


def read_nav_subsystem_lines(file):
    return [l.strip() for l in file.readlines()]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        lines = read_nav_subsystem_lines(f)
        error_score = find_syntax_error_score(lines)
        print(f"Syntax error score: {error_score}")

        autocomplete_score = get_auto_complete_score(lines)
        print(f"Auto-complete score: {autocomplete_score}")

