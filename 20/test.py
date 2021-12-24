import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
                        #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
                        .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
                        .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
                        .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
                        ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
                        ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
                        
                        #..#.
                        #....
                        ##..#
                        ..#..
                        ..###"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_enhanceable_image(f)

    def test_enhance_2(self):
        image = self.parse_input(self.sample_input)
        image.enhance()
        image.enhance()
        self.assertEqual(35, image.lit_pixels)

    def test_enhance_50(self):
        image = self.parse_input(self.sample_input)
        for _ in range(50):
            image.enhance()
        self.assertEqual(3351, image.lit_pixels)
