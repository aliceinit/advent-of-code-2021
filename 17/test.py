import io
import re
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = "target area: x=20..30, y=-10..-5"
    possible_velocities_str = """   23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
                                    25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
                                    8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
                                    26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
                                    20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
                                    25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
                                    25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
                                    8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
                                    24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
                                    7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
                                    23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
                                    27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
                                    8,-2    27,-8   30,-5   24,-7"""
    possible_velocities = [(int(coord.split(",")[0]), int(coord.split(",")[1]))
                           for coord in re.split("\s", possible_velocities_str)
                           if "," in coord]

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_target_area(f)

    def test_input_parse(self):
        self.assertEqual(((20, -10), (30, -5)), self.parse_input(self.sample_input))

    def test_highest_height(self):
        coords = self.parse_input(self.sample_input)
        self.assertEqual(45, calculate_highest_y(*coords))

    def test_does_path_reaches_target_true(self):
        coords = self.parse_input(self.sample_input)
        self.assertTrue(does_path_reach_target((9, 0), *coords))

    def test_does_path_reaches_target_false(self):
        coords = self.parse_input(self.sample_input)
        self.assertFalse(does_path_reach_target((17, -4), *coords))

    def test_all_possible_values(self):
        coords = self.parse_input(self.sample_input)
        velocities = calculate_valid_velocities(*coords)
        self.assertEqual(112, len(velocities))
        self.assertEqual(sorted(self.possible_velocities), sorted(velocities))
