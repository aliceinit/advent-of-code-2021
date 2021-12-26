from heapdict import heapdict
from collections import namedtuple


class DeterministicDie:
    def __init__(self):
        self.number = 0
        self.roll_count = 0

    def roll(self):
        self.roll_count += 1
        self.number = (self.number % 100) + 1
        return self.number


class Player:

    def __init__(self, starting_position):
        self.position = starting_position
        self.score = 0

    def move(self, spaces):
        old_pos = self.position
        self.position = ((self.position + spaces) % 10)
        if self.position == 0:
            self.position = 10
        self.score += self.position


def play_deterministic_game(p1_pos: int, p2_pos: int):
    die = DeterministicDie()
    p1 = Player(p1_pos)
    p2 = Player(p2_pos)
    players = [p1, p2]
    current_player = 0
    while not p1.score >= 1000 and not p2.score >= 1000:
        roll = die.roll() + die.roll() + die.roll()
        players[current_player].move(roll)
        current_player = (current_player + 1) % 2

    # Current player is the loser
    return players[current_player].score * die.roll_count


def get_roll_probabilities():
    rolls = [a + b + c for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]
    roll_counts = {}
    for roll in rolls:
        if roll_counts.get(roll):
            roll_counts[roll] += 1
        else:
            roll_counts[roll] = 1
    return roll_counts


def play_dirac_game(p1_pos: int, p2_pos: int):
    Game = namedtuple("Game", "score1 pos1 score2 pos2 next_player")
    games = heapdict({Game(0, p1_pos, 0, p2_pos, 0): 1})

    multiverse_score = [0, 0]
    roll_counts = get_roll_probabilities()
    multiverse_count = 0
    die_rolls = 0

    while len(games.items()) > 0:
        item = games.popitem()
        game: Game = item[0]
        universe_count: int = item[1]

        if game.score1 >= 21:
            multiverse_count += universe_count
            multiverse_score[0] += universe_count
        elif game.score2 >= 21:
            multiverse_count += universe_count
            multiverse_score[1] += universe_count
        else:
            die_rolls += 27
            for next_roll, new_universes in roll_counts.items():
                if game.next_player == 0:
                    next_pos = (game.pos1 + next_roll) % 10
                    if next_pos == 0:
                        next_pos = 10
                    new_game = Game(game.score1 + next_pos,
                                    next_pos,
                                    game.score2,
                                    game.pos2,
                                    1)
                else:
                    next_pos = (game.pos2 + next_roll) % 10
                    if next_pos == 0:
                        next_pos = 10
                    new_game = Game(game.score1,
                                    game.pos1,
                                    game.score2 + next_pos,
                                    next_pos,
                                    0)
                try:
                    previous_universes = games.pop(new_game)
                except KeyError:
                    previous_universes = 0
                games[new_game] = previous_universes + (universe_count * new_universes)

    print(f"Computed {multiverse_count} universes created from {die_rolls} die rolls ")
    return multiverse_score[0], multiverse_score[1]


def parse_start_positions(file):
    lines = [l.strip().split(" ") for l in file.readlines()]
    return [int(l[-1]) for l in lines]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        positions = parse_start_positions(f)
        res = play_deterministic_game(*positions)
        print(f"Final deterministic game result: {res}")

        p1, p2 = play_dirac_game(*positions)
        if p1 > p2:
            print(f"Player one wins in more universes! ({p1} of {p1 + p2})")
        else:
            print(f"Player two wins in more universes! ({p2} of {p1 + p2})")