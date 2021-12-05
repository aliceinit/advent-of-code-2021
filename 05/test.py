import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """0,9 -> 5,9
                    8,0 -> 0,8
                    9,4 -> 3,4
                    2,2 -> 2,1
                    7,0 -> 7,4
                    6,4 -> 2,0
                    0,9 -> 2,9
                    3,4 -> 1,4
                    0,0 -> 8,8
                    5,5 -> 8,2"""

    @staticmethod
    def parse_input(input_str, exclude_diagonals=False):
        with io.StringIO(input_str) as f:
            vent_lines = parse_vent_lines(f)
            if exclude_diagonals:
                return [v for v in vent_lines if v.type != LineType.DIAGONAL]
            else:
                return vent_lines

    def test_sample_no_diagonals(self):
        vent_lines = self.parse_input(self.sample_input, exclude_diagonals=True)
        overlap_points = count_overlaps(vent_lines)
        assert overlap_points == 5

    def test_sample_with_diagonals(self):
        vent_lines = self.parse_input(self.sample_input, exclude_diagonals=False)
        overlap_points = count_overlaps(vent_lines)
        assert overlap_points == 12

    def test_horizontal_line_increasing(self):
        line = Line(0, 0, 0, 2)
        assert set(line.points) == {(0, 0), (0, 1), (0, 2)}

    def test_horizontal_line_decreasing(self):
        line = Line(0, 2, 0, 0)
        assert set(line.points) == {(0, 0), (0, 1), (0, 2)}

    def test_vertical_line_increasing(self):
        line = Line(0, 0, 2, 0)
        assert set(line.points) == {(0, 0), (1, 0), (2, 0)}

    def test_vertical_line_decreasing(self):
        line = Line(2, 0, 0, 0)
        assert set(line.points) == {(0, 0), (1, 0), (2, 0)}

    def test_single_point_line(self):
        line = Line(0, 0, 0, 0)
        assert set(line.points) == {(0, 0)}

    def test_diagonal_up_right(self):
        line = Line(0, 0, 2, 2)
        assert set(line.points) == {(0, 0), (1, 1), (2, 2)}

    def test_diagonal_up_left(self):
        line = Line(2, 0, 0, 2)
        assert set(line.points) == {(0, 2), (1, 1), (2, 0)}

    def test_diagonal_down_right(self):
        line = Line(0, 2, 2, 0)
        assert set(line.points) == {(0, 2), (1, 1), (2, 0)}

    def test_diagonal_down_left(self):
        line = Line(2, 2, 0, 0)
        assert set(line.points) == {(0, 0), (1, 1), (2, 2)}

