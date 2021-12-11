import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """2199943210
                        3987894921
                        9856789892
                        8767896789
                        9899965678"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return read_floor_map(f)

    def test_sample_input(self):
        floor_map = self.parse_input(self.sample_input)
        low_points = find_low_points(floor_map)
        self.assertEqual(4, len(low_points))
        self.assertEqual(15, sum_risk_levels(low_points))

    def test_risk_calculation(self):
        self.assertEqual(15, sum_risk_levels([0, 1, 5, 5]))
