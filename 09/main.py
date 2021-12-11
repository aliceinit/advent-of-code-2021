def find_low_points(floor_map):
    """
    Finds all points on a floor map which are lower than all adjacent points
    :param floor_map: list of same-length-lists defining coordinates
    :return: list of low-point values
    """
    low_points = []
    for i, row in enumerate(floor_map):
        for j, col in enumerate(row):
            value = floor_map[i][j]
            if value == 0:  # 0 is always a low point
                low_points.append(0)
            elif value < 9:  # 9 is never a low point:
                first_row = i == 0
                last_row = i == len(floor_map) - 1
                first_col = j == 0
                last_col = j == len(row) - 1

                neighbours = filter(lambda val: val is not None,
                                    [  # Get number above
                                        floor_map[i - 1][j] if not first_row else None,
                                        # Get number to the left
                                        floor_map[i][j - 1] if not first_col else None,
                                        # Get number to the right
                                        floor_map[i + 1][j] if not last_row else None,
                                        # Get number below
                                        floor_map[i][j + 1] if not last_col else None
                                    ])
                if all([value < n for n in neighbours]):
                    low_points.append(value)
    return low_points


def sum_risk_levels(values):
    """
    Returns the sum of the risk levels for provided points
        risk level is calculated as the point value + 1
    :param values: list of integers
    :return: int
    """
    return sum([1 + v for v in values])


def read_floor_map(file):
    rows = [row.strip() for row in file.readlines()]
    return [[int(num) for num in row]
            for row in rows]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        floor_map = read_floor_map(f)
        low_points = find_low_points(floor_map)
        print(f"Total Risk Score = {sum_risk_levels(low_points)}")
