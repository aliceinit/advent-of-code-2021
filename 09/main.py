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


def find_basins(floor_map):
    """
    Groups all points on a floor map into basins and calculates the size of the basin
    Basins are groups of numbers bordered by nines (which are not part of any basin)
    :param floor_map: list of same-length-lists defining coordinates
    :return: list of int, representing basin sizes
    """
    basins = {}
    basin_map = [[None] * len(floor_map[0])] * len(floor_map)
    last_basin_id = 0

    def mark_basin(i, j, basin_id, value):
        if not basins.get(basin_id):
            basins[basin_id] = []
        basins[basin_id].append(value)
        basin_map[i][j] = basin_id

    for i, row in enumerate(floor_map):
        for j, col in enumerate(row):
            value = floor_map[i][j]

            if value == 9:  # we are not part of a basin
                basin_map[i][j] = None
            else:
                first_row = i == 0
                first_col = j == 0

                # Only look up and left
                previous_neighbours = list(filter(lambda val: val is not None,
                                                  [  # Get number above
                                                      basin_map[i - 1][j] if not first_row else None,
                                                      # Get number to the left
                                                      basin_map[i][j - 1] if not first_col else None
                                                  ]))
                if len(previous_neighbours) == 0:
                    # Neither neighbour is part of a basin -- start tracking a new one
                    last_basin_id += 1
                    mark_basin(i, j, last_basin_id, value)

                elif len(previous_neighbours) == 1 or \
                        previous_neighbours[0] == previous_neighbours[1]:
                    # One of both of our neighbors are in a basin: add ourself to the same basin
                    mark_basin(i, j, previous_neighbours[0], value)
                elif previous_neighbours[0] != previous_neighbours[1]:
                    # Our neighbours which were thought to be in different basins are actually
                    # Part of the same basin: merge them and add ourselves
                    mark_basin(i, j, previous_neighbours[0], value)
                    basins[previous_neighbours[0]] += basins[previous_neighbours[1]]
                    basins.pop(previous_neighbours[1])
                    for x in range(0, i):
                        for y in range(0, j):
                            if basin_map[x][y] == previous_neighbours[1]:
                                basin_map[x][y] = previous_neighbours[0]

    return sorted([len(basin_vals)
                   for basin_vals in basins.values()], reverse=True)


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
        basins = find_basins(floor_map)
        print(f"Three biggest basins: {basins[0:3]} (multiplied = {basins[0] * basins[1] * basins[2]})")