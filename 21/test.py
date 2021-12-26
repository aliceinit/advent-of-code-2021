import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  Player 1 starting position: 4
                        Player 2 starting position: 8"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_start_positions(f)

    def test_play_deterministic_sample(self):
        start_positions = self.parse_input(self.sample_input)
        game_result = play_deterministic_game(*start_positions)
        self.assertEqual(739785, game_result)

    def test_diract_sample(self):
        start_positions = self.parse_input(self.sample_input)
        p1_win_count, p2_win_count = play_dirac_game(*start_positions)
        self.assertEqual(444356092776315, p1_win_count)
        self.assertEqual(341960390180808, p2_win_count)

    def test_roll_probabilities(self):
        probs = get_roll_probabilities()
        self.assertEqual(27, sum(probs.values()))
