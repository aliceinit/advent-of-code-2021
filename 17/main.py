def is_position_in_target(position, target_min, target_max):
    x, y = position
    x1, y1 = target_min
    x2, y2 = target_max
    return x1 <= x <= x2 and y1 <= y <= y2


def does_path_reach_target(velocity, min_coord, max_coord):
    pos_x, pos_y = 0, 0
    vx, vy = velocity
    min_x, min_y = min_coord
    max_x, max_y = max_coord

    while pos_x <= max_x and pos_y >= min_y:
        if is_position_in_target((pos_x, pos_y), min_coord, max_coord):
            return True
        pos_x += vx
        if vx != 0:
            vx = vx - 1 if vx > 0 else vx + 1
        pos_y += vy
        vy -= 1

    return False


def calculate_valid_velocities(min_coord, max_coord):
    min_x, min_y = min_coord
    max_x, max_y = max_coord

    # Calculate max & min velocities
    max_y_velocity = abs(min_y) - 1
    min_y_veloxity = min_y
    max_x_velocity = max_x + 1

    x_pos = 0
    min_x_velocity = 0
    while x_pos < min_x:
        min_x_velocity += 1
        x_pos += min_x_velocity

    possible_velocities = []

    # Check which possible velocities reach the target range
    for x in range(min_x_velocity, max_x_velocity + 1):
        for y in range(min_y_veloxity, max_y_velocity + 1):
            if does_path_reach_target((x, y), min_coord, max_coord):
                possible_velocities.append((x, y))

    return possible_velocities


def calculate_highest_y(min_coord, _):
    _, min_y = min_coord
    max_height = 0
    for i in range(1, abs(min_y)):
        max_height += i

    return max_height


def parse_target_area(file):
    input_str = file.read().split(": ")
    x_bound_str, y_bound_str = input_str[1].split(", ")
    xi, xf = (int(x) for x in x_bound_str[2:].split(".."))
    yi, yf = (int(y) for y in y_bound_str[2:].split(".."))
    return (xi, yi), (xf, yf)


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        target_area = parse_target_area(f)
        max_height = calculate_highest_y(*target_area)
        print(f"Highest height while reaching target = {max_height}")

        all_valid_velocities = calculate_valid_velocities(*target_area)
        print(f"Number of possible velocities = {len(all_valid_velocities)}")
