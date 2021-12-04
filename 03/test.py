import io
from unittest import TestCase
from utils.inputs import readlines_as_int
from .main import *


class TestSubCommands(TestCase):
    sample_input = """00100
                    11110
                    10110
                    10111
                    10101
                    01111
                    00111
                    11100
                    10000
                    11001
                    00010
                    01010"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return [line.strip() for line in f.readlines()]

    def test_count_ones(self):
        report = self.parse_input(self.sample_input)
        assert count_ones(report) == [7, 5, 8, 7, 5]

    def test_sample_gamma(self):
        report = self.parse_input(self.sample_input)
        gamma_rate = calculate_gamma_rate(report)
        assert gamma_rate == 22

    def test_sample_epsilon(self):
        report = self.parse_input(self.sample_input)
        epsilon_rate = calculate_epsilon_rate(report)
        assert epsilon_rate == 9

    def test_build_bit_masks(self):
        assert build_bit_masks(1) == [1]
        assert build_bit_masks(2) == [2, 1]
        assert build_bit_masks(6) == [32, 16, 8, 4, 2, 1]

    def test_oxygen_rating(self):
        report = self.parse_input(self.sample_input)
        oxygen = calculate_oxygen_generator_rating(report)
        assert oxygen == 23

    def test_oxygen_rating_with_ties(self):
        report = self.parse_input(
            """111
            000"""
        )
        assert calculate_oxygen_generator_rating(report) == int("111", 2)

    def test_co2_rating(self):
        report = self.parse_input(self.sample_input)
        co2 = calculate_co2_scrubber_rating(report)
        assert co2 == 10

    def test_co2_rating_with_ties(self):
        report = self.parse_input(
            """111
            000"""
        )
        assert calculate_co2_scrubber_rating(report) == int("000", 2)
