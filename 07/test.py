import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """16,1,2,0,4,2,7,1,2,14"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_positions(f)

    def test_sample_min_fuel(self):
        positions = self.parse_input(self.sample_input)
        assert calculate_min_fuel_to_align(positions) == 37

    def test_even_number(self):
        positions = self.parse_input("1,2,9,10")
        assert calculate_min_fuel_to_align(positions) == 16

    def test_skewed_numbers(self):
        positions = self.parse_input("1,2,10")
        assert calculate_min_fuel_to_align(positions) == 9
