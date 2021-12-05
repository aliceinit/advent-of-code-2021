from utils.inputs import readlines_as_int
import re
from operator import add
import functools


class BingoBoard:

    def __init__(self, numbers):
        if not len(numbers) == 25:
            raise AttributeError(f"Bingo Board must be initialized with exactly 25 numbers (got {len(numbers)})")
        self.unmarked = set(numbers)
        self.index_lookup = {num: i for i, num in enumerate(numbers)}
        self.marked_indices = []

    def check_number(self, number):
        """
        Checks if the board contains number & marks it if so
        Checks if the board has won the game
        :param number:
        :return: int, score if game is won, else None
        """
        if number in self.unmarked:
            self.unmarked.remove(number)
            self.marked_indices.append(self.index_lookup.get(number))

        if self.check_win():
            return self.calculate_score(number)
        else:
            return None

    def check_win(self):
        """
        Checks if win condition is met
        :return: boolean

        0  1  2  3  4
        5  6  7  8  9
        10 11 12 13 14
        15 16 17 18 19
        20 21 22 23 24
        """

        # Lets start doing this simple and slow & see if we need to do it better later
        rows = [
            range(0, 5),
            range(5, 10),
            range(10, 15),
            range(15, 20),
            range(20, 25)
        ]
        cols = [
            range(0, 21, 5),
            range(1, 22, 5),
            range(2, 23, 5),
            range(3, 24, 5),
            range(4, 25, 5)
        ]
        for combo in rows + cols:
            if all([i in self.marked_indices for i in combo]):
                return True
        return False

    def calculate_score(self, winning_move):
        return functools.reduce(add, self.unmarked) * winning_move


def play(random_numbers, boards):
    """
    Applies random inputs to all bingo boards to determine the winner
    :param random_numbers: list of ints
    :param boards: list of bingo boards
    :return: tuple(int, int), the winning board # & the winning score
    """
    for rn in random_numbers:
        for i, b in enumerate(boards):
            score = b.check_number(rn)
            if score:
                return i + 1, score


def play_to_the_end(random_numbers, boards):
    """
    Applies random inputs to all bingo boards to determine which board wins last
    :param random_numbers: list of ints
    :param boards: list of bingo boards
    :return: tuple(int, int), the losing board & its final score
    """
    winners = []

    for rn in random_numbers:
        for i, b in enumerate(boards):
            # Don't keep marking numbers on boards that have already won
            if i not in winners:
                score = b.check_number(rn)
                if score:
                    # Check if this is the last board to win
                    if len(winners) == len(boards) - 1:
                        return i + 1, score
                    else:
                        winners.append(i)


def parse_bingo_input(file):
    lines = [line.strip() for line in file]
    random_numbers = [int(n) for n in lines[0].split(",")]
    numbers = []
    boards = []

    for line in lines[1:]:
        numbers += [int(n) for n in re.split("\s+", line)
                    if line]
        if len(numbers) == 25:
            boards.append(BingoBoard(numbers))
            numbers = []

    return random_numbers, boards


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        numbers, boards = parse_bingo_input(f)
        winner, winning_score = play(numbers, boards)
        print(f"Board {winner} won with score {winning_score}")

        loser, losing_score = play_to_the_end(numbers, boards)
        print(f"Board {loser} won last with score {losing_score}")
