from utils.inputs import readlines_as_int


def count_ones(diagnostic_report):
    """
    takes a list of binary numbers as strings and counts how many ones appear
    in each position across all numbers
    :param diagnostic_report: list of binary numbers represented as strings
    :return: list of numbers with length = length of each row of the diagnstic report
             each list value represents the number of ones seen in each position
    """
    one_count = [0 for _ in diagnostic_report[0]]

    for num in diagnostic_report:
        for i, bit in enumerate(num):
            if bit == "1":
                one_count[i] += 1

    return one_count


def calculate_gamma_rate(diagnostic_report):
    """
    Calculates gamma rate from a diagnostic report
    Gamma rate is a new number which uses the most common bit for each position
    across all binary numbers in the diagnostic report
    :param diagnostic_report: list of binary numbers, represented as strings
    :return: int (decimal), gamma rate
    """
    one_counts = count_ones(diagnostic_report)
    sample_size = len(diagnostic_report)

    return int("".join(["1"
                        if count > sample_size / 2
                        else "0"
                        for count in one_counts]), 2)


def calculate_epsilon_rate(diagnostic_report):
    """
    Calculates epsilon rate from a diagnostic report
    Epsilon rate is a new number which uses the least common bit for each position
    across all binary numbers in the diagnostic report
    :param diagnostic_report: list of binary numbers, represented as strings
    :return: int (decimal), epsilon rate
    """
    one_counts = count_ones(diagnostic_report)
    sample_size = len(diagnostic_report)

    return int("".join(["0"
                        if count > sample_size / 2
                        else "1"
                        for count in one_counts]), 2)


def build_bit_masks(bin_length):
    masks = [[0] * bin_length for _ in range(bin_length)]

    for i in range(bin_length):
        masks[i][i] = 1

    string_masks = ["".join([str(s) for s in bits]) for bits in masks]
    return [int(s, 2) for s in string_masks]


def calculate_oxygen_generator_rating(diagnostic_report):
    """
    Calculates Oxygen Generator rating from a diagnostic report
    Calculated by
    :param diagnostic_report: list of binary numbers, represented as strings
    :return: int (dec), Oxygen generator rating
    """
    masks = build_bit_masks(len(diagnostic_report[0]))
    binary_numbers = [int(s, 2)
                      for s in diagnostic_report]
    for m in masks:
        ones = []
        zeros = []

        for b in binary_numbers:
            if b & m:
                ones.append(b)
            else:
                zeros.append(b)
        if len(zeros) > len(ones):
            binary_numbers = zeros
        else:
            binary_numbers = ones
    return binary_numbers[0]


def calculate_co2_scrubber_rating(diagnostic_report):
    """
    Calculates CO2 Scrubber Rating rating from a diagnostic report
    Calculated by
    :param diagnostic_report: list of binary numbers, represented as strings
    :return: int (dec), CO2 Scrubber rating
    """
    masks = build_bit_masks(len(diagnostic_report[0]))
    binary_numbers = [int(s, 2)
                      for s in diagnostic_report]
    for m in masks:
        if len(binary_numbers) == 1:
            return binary_numbers[0]

        ones = []
        zeros = []

        for b in binary_numbers:
            if b & m:
                ones.append(b)
            else:
                zeros.append(b)
        if len(zeros) > len(ones):
            binary_numbers = ones
        else:
            binary_numbers = zeros
    return binary_numbers[0]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        report = [line.strip() for line in f.readlines()]
        gamma = calculate_gamma_rate(report)
        epsilon = calculate_epsilon_rate(report)
        print(f"Gamma x Epsilon = {gamma * epsilon}")

        oxygen = calculate_oxygen_generator_rating(report)
        co2 = calculate_co2_scrubber_rating(report)
        print(f"O x CO2 ratings = {oxygen * co2}")
