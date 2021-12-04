from utils.inputs import readlines_as_int


def move(commands, initial_depth=0, initial_horizontal_position=0):
    """
    Calculates final position after applying commands to the initial position
    :param commands: pairs of directions (forward, up, or down) & integers
    :param initial_depth: int, defaults to 0
    :param initial_horizontal_position: int, defaults to 0
    :return: tuple (depth, horizontal position)
    """
    depth = initial_depth
    h_pos = initial_horizontal_position

    for command, distance in commands:
        if command == "forward":
            h_pos = h_pos + distance
        elif command == "up":
            depth = depth - distance
        elif command == "down":
            depth = depth + distance
        else:
            raise ValueError(f"Unrecognized command {command}")

    return depth, h_pos

def move_with_aim(commands, initial_depth=0, initial_horizontal_position=0):
    """
    Calculates final aim position based on commands
    :param commands: pairs of directions (forward, up, or down) & integers
    :param initial_depth: int, defaults to 0
    :param initial_horizontal_position: int, defaults to 0
    :return: tuple, (depth, horizontal position)
    """
    depth = initial_depth
    h_pos = initial_horizontal_position
    aim = 0

    for command, amount in commands:
        if command == "forward":
            h_pos = h_pos + amount
            depth = depth + (aim * amount)
        elif command == "up":
            aim = aim - amount
        elif command == "down":
            aim = aim + amount
        else:
            raise ValueError(f"Unrecognized command {command}")

    return depth, h_pos


def read_sub_commands(file):
    string_pairs = [line.strip().split(" ") for line in file.readlines()]
    return [(s[0], int(s[1])) for s in string_pairs]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        commands = read_sub_commands(f)
        final_pos = move(commands)
        final_correct_pos = move_with_aim(commands)
        print(f"Final position vals multiplied = {final_pos[0] * final_pos[1]}")
        print(f"Final correct position vals multiplied = {final_correct_pos[0] * final_correct_pos[1]}")
