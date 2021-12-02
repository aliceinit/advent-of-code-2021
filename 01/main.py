from utils.inputs import readlines_as_int


def count_increasing(num_list):
    count = 0

    for i, num in enumerate(num_list[1:]):
        if num > num_list[i]:
            count = count + 1
    return count


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        increasing = count_increasing(readlines_as_int(f))
        print(f"Number of times inputs increased: {increasing}")
