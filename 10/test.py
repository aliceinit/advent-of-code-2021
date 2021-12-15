import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  [({(<(())[]>[[{[]{<()<>>
                        [(()[<>])]({[<{<<[]>>(
                        {([(<{}[<>[]}>{[]{[(<()>
                        (((({<>}<{<{<>}{[]{[]{}
                        [[<[([]))<([[{}[[()]]]
                        [{[{({}]{}}([{[{{{}}([]
                        {<[[]]>}<{[{[{[]{()[[[]
                        [<(<(<(<{}))><([]([]()
                        <{([([[(<>()){}]>(<<{{
                        <{([{{}}[<[[[<>{}]]]>[]]   """

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return read_nav_subsystem_lines(f)

    def test_sample_input_error_score(self):
        lines = self.parse_input(self.sample_input)
        score = find_syntax_error_score(lines)
        self.assertEqual(26397, score)

