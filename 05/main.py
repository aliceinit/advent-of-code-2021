from enum import Enum


class LineType(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
    DIAGONAL = 3


class Line:

    def __init__(self, x1, y1, x2, y2):
        if x1 == x2:
            self.type = LineType.HORIZONTAL
        elif y1 == y2:
            self.type = LineType.VERTICAL
        else:
            self.type = LineType.DIAGONAL

        x_range = range(x1, x2 + 1) if x2 > x1 else range(x1, x2 - 1, -1)
        y_range = range(y1, y2 + 1) if y2 > y1 else range(y1, y2 - 1, -1)

        if self.type == LineType.DIAGONAL:
            if len(x_range) != len(y_range):
                raise AttributeError("Not supported by hydrothermal vent system!")
            self.points = []
            for i in range(0, len(x_range)):
                self.points.append((x_range[i], y_range[i]))
        else:
            self.points = [(x, y)
                           for x in x_range
                           for y in y_range]

    def __repr__(self):
        return str(self.points)


def parse_vent_lines(file):
    """
    Takes puzzle input of coordinate pairs and returns
    :param file: puzzle input file
    :return: List of Lines
    """
    file_lines = [line.strip() for line in file.readlines()]
    vent_lines = []

    for line in file_lines:
        coordinates = line.split("->")
        coordinate_1 = [int(n.strip()) for n in coordinates[0].split(",")]
        coordinate_2 = [int(n.strip()) for n in coordinates[1].split(",")]
        vent_lines.append(Line(
            x1=coordinate_1[0],
            y1=coordinate_1[1],
            x2=coordinate_2[0],
            y2=coordinate_2[1]
        ))

    return vent_lines


def count_overlaps(lines):
    """
    Counts the number of coordinates where at least two lines overlap
    :param lines: list of Line objects
    :return: int, count of overlap points
    """
    counts = {}
    for line in lines:
        for point in line.points:

            if not counts.get(str(point)):
                counts[str(point)] = 1
            else:
                counts[str(point)] += 1

    count_of_counts = 0

    for count in counts.values():
        if count > 1:
            count_of_counts += 1

    return count_of_counts


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        vent_lines = parse_vent_lines(f)
        vent_lines_no_diagonals = [v for v in vent_lines if v.type != LineType.DIAGONAL]
        overlap_points = count_overlaps(vent_lines_no_diagonals)
        print(f"Number of points where two or more lines overlap: {overlap_points}")

        overlap_with_diagonals = count_overlaps(vent_lines)
        print(f"Number of overlaps including diagonals: {overlap_with_diagonals}")
