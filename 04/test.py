import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

            22 13 17 11  0
             8  2 23  4 24
            21  9 14 16  7
             6 10  3 18  5
             1 12 20 15 19

             3 15  0  2 22
             9 18 13 17  5
            19  8  7 25 23
            20 11 10 24  4
            14 21 16 12  6

            14 21 17 24  4
            10 16 15  9 19
            18  8 23 26 20
            22 11 13  6  5
             2  0 12  3  7
            """

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_bingo_input(f)

    def test_parse_sample_input(self):
        random_numbers, boards = self.parse_input(self.sample_input)
        assert len(boards) == 3
        assert isinstance(boards[0], BingoBoard)
        assert random_numbers[0] == 7
        assert random_numbers[-1] == 1

    def test_sample_game(self):
        random_numbers, boards = self.parse_input(self.sample_input)
        winner, score = play(random_numbers, boards)
        assert winner == 3
        assert score == 4512

    def test_sample_to_the_end(self):
        random_numbers, boards = self.parse_input(self.sample_input)
        loser, score = play_to_the_end(random_numbers, boards)

        assert loser == 2
        assert score == 1924