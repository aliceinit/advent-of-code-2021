import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """3,4,3,1,2"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_lanternfish(f)

    def test_sample_fish(self):
        fish = self.parse_input(self.sample_input)
        fish_after_80 = simulate_fish_population(80, fish)
        fish_after_256 = simulate_fish_population(256, fish)
        assert fish_after_80 == 5934
        assert fish_after_256 == 26984457539

