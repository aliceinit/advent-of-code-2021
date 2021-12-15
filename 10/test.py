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

    def test_sample_input_find_incomplete(self):
        lines = self.parse_input(self.sample_input)
        incomplete_lines = get_incomplete_lines(lines)
        self.assertEqual(["[({(<(())[]>[[{[]{<()<>>",
                          "[(()[<>])]({[<{<<[]>>(",
                          "(((({<>}<{<{<>}{[]{[]{}",
                          "{<[[]]>}<{[{[{[]{()[[[]",
                          "<{([{{}}[<[[[<>{}]]]>[]]"],
                         ["".join(line) for line in incomplete_lines])

    def test_sample_autocomplete(self):
        self.assertEqual("}}]])})]",
                         "".join(autocomplete_line("[({(<(())[]>[[{[]{<()<>>")))

    def test_autocomplete_line_score(self):
        self.assertEqual(288957,
                         get_auto_complete_line_score("[({(<(())[]>[[{[]{<()<>>"))

    def test_sample_input_find_autocomplete_score(self):
        lines = self.parse_input(self.sample_input)
        self.assertEqual(288957,
                         get_auto_complete_score(lines))

    def test_return_middle_val(self):
        self.assertEqual(3, return_middle_val([1, 2, 3, 4, 5]))
        self.assertEqual(4, return_middle_val([1, 2, 3, 4, 5, 6, 7]))
        self.assertEqual(5, return_middle_val([1, 2, 3, 4, 5, 6, 7, 8, 9]))
