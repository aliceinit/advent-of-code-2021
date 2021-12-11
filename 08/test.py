import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input_big = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
                        edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
                        fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
                        fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
                        aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
                        fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
                        dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
                        bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
                        egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
                        gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

    sample_input_small = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return read_digit_displays(f)

    def test_sample_count_easy_digits(self):
        displays = self.parse_input(self.sample_input_big)
        assert count_easy_digits(displays) == 26

    def test_find_segment_key(self):
        sample_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
        legend, _ = self.parse_input(sample_line)[0]
        self.assertEqual({"d": "a",
                          "e": "b",
                          "a": "c",
                          "f": "d",
                          "g": "e",
                          "b": "f",
                          "c": "g"}, find_segment_key(legend))

    def test_find_digit_key(self):
        sample_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
        legend, _ = self.parse_input(sample_line)[0]
        assert find_digit_key(legend) == {"abcdefg": 8,
                                          "bcdef": 5,
                                          "acdfg": 2,
                                          "abcdf": 3,
                                          "abd": 7,
                                          "abcdef": 9,
                                          "bcdefg": 6,
                                          "abef": 4,
                                          "abcdeg": 0,
                                          "ab": 1}

    def test_find_solution(self):
        sample_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
        legend, display = self.parse_input(sample_line)[0]
        assert decode_display(legend, display) == 5353

    def test_find_solution_big_example(self):
        displays = self.parse_input(self.sample_input_big)

        self.assertEqual([8394,
                          9781,
                          1197,
                          9361,
                          4873,
                          8418,
                          4548,
                          1625,
                          8717,
                          4315], [decode_display(l, d) for l, d in displays])
