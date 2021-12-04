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
    :param diagnostic_report: list of numbers
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
    :param diagnostic_report: list of numbers
    :return: int (decimal), epsilon rate
    """
    one_counts = count_ones(diagnostic_report)
    sample_size = len(diagnostic_report)

    return int("".join(["0"
                        if count > sample_size / 2
                        else "1"
                        for count in one_counts]), 2)


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        report = [line.strip() for line in f.readlines()]
        gamma = calculate_gamma_rate(report)
        epsilon = calculate_epsilon_rate(report)
        print(f"Gamma x Epsilon = {gamma * epsilon}")
