import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  6,10
                        0,14
                        9,10
                        0,3
                        10,4
                        4,11
                        6,0
                        6,12
                        4,1
                        0,13
                        10,12
                        3,4
                        3,0
                        8,4
                        1,10
                        2,14
                        8,10
                        9,0
                        
                        fold along y=7
                        fold along x=5"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_chart_and_folds(f)

    @staticmethod
    def dot_graph_from_graphical_string(dot_graph_string):
        """Transforms example diagrams into readable format"""
        dots = set()
        lines = [[c for c in l.strip()] for l in dot_graph_string.split("\n")]

        # Parse chars into 2d array
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    dots.add((x, y))
        return dots

    def test_sample_parse_data(self):
        dot_chart, fold_instructions = self.parse_input(self.sample_input)
        self.assertEqual([("y", 7), ("x", 5)], fold_instructions)
        self.assertEqual(self.dot_graph_from_graphical_string("""   ...#..#..#.
                                                                    ....#......
                                                                    ...........
                                                                    #..........
                                                                    ...#....#.#
                                                                    ...........
                                                                    ...........
                                                                    ...........
                                                                    ...........
                                                                    ...........
                                                                    .#....#.##.
                                                                    ....#......
                                                                    ......#...#
                                                                    #..........
                                                                    #.#........"""),
                         dot_chart)

    def test_minimal_y_fold(self):
        chart = self.dot_graph_from_graphical_string("""...
                                                        ...
                                                        ...
                                                        ...
                                                        ...
                                                        .#.
                                                        ###""")
        new_chart = perform_fold(chart, ("y", 3))
        self.assertEqual({(0, 0), (1, 0), (2, 0), (1, 1)}, new_chart)

    def test_minimal_x_fold(self):
        chart = self.dot_graph_from_graphical_string("""......#
                                                        .....##
                                                        ......#""")
        new_chart = perform_fold(chart, ("x", 3))
        self.assertEqual({(0, 0), (0, 1), (0, 2), (1, 1)}, new_chart)

    def test_sample_first_fold(self):
        dot_chart, fold_instructions = self.parse_input(self.sample_input)
        new_chart = perform_fold(dot_chart, fold_instructions[0])
        self.assertEqual(self.dot_graph_from_graphical_string("""   #.##..#..#.
                                                                    #...#......
                                                                    ......#...#
                                                                    #...#......
                                                                    .#.#..#.###
                                                                    ...........
                                                                    ..........."""),
                         new_chart)
