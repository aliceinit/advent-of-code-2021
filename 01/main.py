from utils.inputs import readlines_as_int


def count_increasing(num_list):
    """
    :param num_list: list of integers
    :return: the number of items greater than the previous item
    """
    count = 0

    for i, num in enumerate(num_list[1:]):
        if num > num_list[i]:
            count = count + 1
    return count


def sum_batches_of_three(num_list):
    """
    For a list of integers, returns a new list that is the sum i + (i+1) + (1+2)
    for each index (except the last two indices)
    e.g. [1, 2, 3, 4, 5, 6, 7] => [6, 15]

    :param num_list: list of integers
    :return: new list of integers
    """
    return [
        num + num_list[i + 1] + num_list[i + 2]
        for i, num in enumerate(num_list)
        if i < len(num_list) - 2
    ]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        int_list = readlines_as_int(f)
        increasing = count_increasing(int_list)
        print(f"Number of times inputs increased: {increasing}")
        batched_input = sum_batches_of_three(int_list)
        print(f"Recount after batching: {count_increasing(batched_input)}")
