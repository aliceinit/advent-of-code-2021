import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  1163751742
                        1381373672
                        2136511328
                        3694931569
                        7463417111
                        1319128137
                        1359912421
                        3125421639
                        1293138521
                        2311944581"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_cave_paths(f)

    def test_sample_data(self):
        least_risk = find_best_path(*self.parse_input(self.sample_input))
        self.assertEqual(40, least_risk)

    def test_counter_example_to_greedy(self):
        start_node, end_node = self.parse_input("""  1911
                                                     7991
                                                     9991""")
        least_risk = find_best_path(start_node, end_node)
        self.assertEqual(13, least_risk)
