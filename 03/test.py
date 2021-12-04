import io
from unittest import TestCase
from utils.inputs import readlines_as_int
from .main import calculate_gamma_rate, calculate_epsilon_rate, count_ones


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
