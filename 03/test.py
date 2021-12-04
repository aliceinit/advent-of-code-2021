import io
from unittest import TestCase
from .main import move, read_sub_commands, move_with_aim


class TestSubCommands(TestCase):
    sample_input = """forward 5
                      down 5
                      forward 8
                      up 3
                      down 8
                      forward 2"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return read_sub_commands(f)

    def test_parse_input(self):
        parsed = self.parse_input(self.sample_input)
        assert parsed[0] == ("forward", 5)
        assert len(parsed) == 6
        assert parsed[5] == ("forward", 2)

    def test_sample_move(self):
        parsed = self.parse_input(self.sample_input)
        depth, h_pos = move(parsed)
        assert depth == 10
        assert h_pos == 15

    def test_sample_move_with_aim(self):
        parsed = self.parse_input(self.sample_input)
        depth, h_pos = move_with_aim(parsed)
        assert depth == 60
        assert h_pos == 15
