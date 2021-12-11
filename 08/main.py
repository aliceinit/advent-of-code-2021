expected_display = {
    # length = 2
    1: ["c", "f"],
    # length = 3
    7: ["a", "c", "f"],
    # length = 4
    4: ["b", "c", "d", "f"],
    # length = 5 ; <- need to disambiguate between 2, 3, and 5
    2: ["a", "c", "d", "e", "g"],
    3: ["a", "c", "d", "f", "g"],
    5: ["a", "b", "d", "f", "g"],
    # length = 6 ; <- need to disambiguate between 0, 6, and 9
    0: ["a", "b", "c", "e", "f", "g"],
    6: ["a", "b", "d", "e", "f", "g"],
    9: ["a", "b", "c", "d", "f", "g"],
    # length = 7
    8: ["a", "b", "c", "d", "e", "f", "g"],
}
segment_combos_to_int = {
    "".join(sorted(letter_list)): num
    for num, letter_list in expected_display.items()
}

# Lookup for numbers which can be identified by length
numbers_by_length = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}


def read_digit_displays(file):
    displays = []
    for line in file.readlines():
        legend, output = line.split("|")
        displays.append(
            (
                legend.strip().split(" "),
                output.strip().split(" ")
            )
        )
    return displays


def count_easy_digits(displays):
    """Count how many times 1, 4, 7, or 8 appear in output values of displays"""
    count = 0

    for _, outputs in displays:
        for digit in outputs:
            if numbers_by_length.get(len(digit)):
                count += 1

    return count


def find_segment_key(legend):
    sorted_legend = [set(digit) for digit in sorted(legend, key=lambda x: len(x))]
    # we always know a and the remainder can be narrowed to two possibilities
    b_or_d = sorted_legend[2] - sorted_legend[0]
    e_or_g = sorted_legend[-1] - sorted_legend[1] - sorted_legend[2]
    segment_key = {"a": sorted_legend[1] - sorted_legend[0],
                   "b": b_or_d,
                   "c": sorted_legend[0],
                   "d": b_or_d,
                   "e": e_or_g,
                   "f": sorted_legend[0],
                   "g": e_or_g}

    # disambiguate segments using numbers where they appear without their pairs
    len_six_digits = sorted_legend[6:-1]
    for d in len_six_digits:
        g_value = segment_key["g"] & d
        f_value = segment_key["f"] & d
        b_value = segment_key["b"] & d

        if len(f_value) == 1:
            segment_key["f"] = f_value
            segment_key["c"] = segment_key["c"] - f_value
        if len(g_value) == 1:
            segment_key["g"] = g_value
            segment_key["e"] = segment_key["e"] - g_value
        if len(b_value) == 1:
            segment_key["b"] = b_value
            segment_key["d"] = segment_key["d"] - b_value

    # Flip result for easy lookup in reverse direction
    return {list(set_of_letters)[0]: letter for letter, set_of_letters in segment_key.items()}


def find_digit_key(legend):
    segment_key = find_segment_key(legend)
    sorted_legend = ["".join(sorted([segment for segment in digit]))
                     for digit in legend]
    translated = {digit: "".join(sorted([segment_key[letter] for letter in digit]))
                  for digit in sorted_legend}
    return {digit: segment_combos_to_int[translated_digit]
            for digit, translated_digit in translated.items()}


def decode_display(legend, display):
    digit_key = find_digit_key(legend)
    sorted_display = ["".join(sorted([segment for segment in digit]))
                      for digit in display]
    return (digit_key[sorted_display[0]] * 1000
            + digit_key[sorted_display[1]] * 100
            + digit_key[sorted_display[2]] * 10
            + digit_key[sorted_display[3]])


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        displays = read_digit_displays(f)
        easy_digits = count_easy_digits(displays)
        print(f"Number of easy digits in outputs: {easy_digits}")

        decoded_displays = [decode_display(legend, display)
                            for legend, display in displays]
        displays_sum = sum(decoded_displays)
        print(f"Total sum of decoded displays: {displays_sum}")
