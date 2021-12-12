import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  2199943210
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

    def test_find_basins_sample(self):
        floor_map = self.parse_input(self.sample_input)
        basins = find_basins(floor_map)
        self.assertEqual([14, 9, 9, 3],
                         basins)

    def test_find_basins_tricky(self):
        input = """ 00900
                    00900
                    90009
                    00900
                    00900"""
        floor_map = self.parse_input(input)
        basins = find_basins(floor_map)
        self.assertEqual([19], basins)

    def test_find_basins_multiple(self):
        input = """ 00900
                    00900
                    99999
                    00900
                    00900"""
        floor_map = self.parse_input(input)
        basins = find_basins(floor_map)
        self.assertEqual([4, 4, 4, 4], basins)
