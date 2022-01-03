import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_simple = """ ...>...
                        .......
                        ......>
                        v.....>
                        ......>
                        .......
                        ..vvv.."""
    sample_start = """  v...>>.vv>
                        .vv>>.vv..
                        >>.>v>...v
                        >>v>>.>.v.
                        v>v.vv.v..
                        >.>>..v...
                        .vv..>.>v.
                        v.v..>>v.v
                        ....v..v.>"""
    sample_stalled = """..>>v>vv..
                        ..v.>>vv..
                        ..>>v>>vv.
                        ..>>>>>vv.
                        v......>vv
                        v>v....>>v
                        vvv.....>>
                        >vv......>
                        .>v.vv.v.."""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_ocean_floor(f)

    def test_simple_single_round(self):
        cucumbers = self.parse_input(self.sample_simple)
        moves = move_cucumbers(cucumbers)
        print(cucumbers)
        self.assertTrue(moves)

    def test_sample_stalled(self):
        cucumbers = self.parse_input(self.sample_stalled)
        moves = move_cucumbers(cucumbers)
        self.assertFalse(moves)

    def test_sample_until_deadlock(self):
        cucumbers = self.parse_input(self.sample_start)
        moves = move_cucumbers_until_deadlock(cucumbers)
        self.assertEqual(58, moves + 1)
