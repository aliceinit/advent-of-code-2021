import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
    solved_state = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_amphipod_burrow(f)

    def test_base_case_least_energy(self):
        solved_state = self.parse_input(self.solved_state)
        least_energy, pos = solved_state.organize()
        self.assertEqual(0, least_energy)

    def test_move_from_room_to_room(self):
        simple_input = """#############
#.....C.....#
###A#B#D#.###
  #A#B#C#D#
  #########"""
        burrow = self.parse_input(simple_input)
        self.assertIsNone(burrow.initial_amphipods.get((9, 2)))
        e = burrow.move_amphipods_home(burrow.initial_amphipods)
        self.assertEqual(4000, e)
        self.assertEqual("D", burrow.initial_amphipods.get((9, 2)))

    def test_move_multiple_rounds_to_room(self):
        simple_input = """#############
#...C.D.....#
###A#B#.#.###
  #A#B#C#D#
  #########"""
        burrow = self.parse_input(simple_input)
        self.assertIsNone(burrow.initial_amphipods.get((7, 2)))
        self.assertIsNone(burrow.initial_amphipods.get((9, 2)))
        e, pos = burrow.organize()
        self.assertEqual(4400, e)
        self.assertEqual("C", pos.get((7, 2)))
        self.assertEqual("D", pos.get((9, 2)))

    def test_move_from_hallway_to_room(self):
        simple_input = """#############
#.....C.....#
###A#B#.#D###
  #A#B#C#D#
  #########"""
        burrow = self.parse_input(simple_input)
        self.assertIsNone(burrow.initial_amphipods.get((7, 2)))
        e = burrow.move_amphipods_home(burrow.initial_amphipods)
        self.assertEqual(200, e)
        self.assertEqual("C", burrow.initial_amphipods.get((7, 2)))

    def test_no_moves_to_room(self):
        simple_input = """#############
#.A.D...C.B.#
###.#.#B#.###
  #D#A#C#D#
  #########"""
        burrow = self.parse_input(simple_input)
        amphipod_positions = burrow.initial_amphipods
        self.assertIsNone(burrow.initial_amphipods.get((5, 2)))
        e = burrow.move_amphipods_home(burrow.initial_amphipods)
        self.assertEqual(0, e)
        self.assertIsNone(amphipod_positions.get((5, 2)))

    def test_least_energy_used(self):
        simple_input = """#############
#.........C.#
###B#A#D#.###
  #A#B#C#D#
  #########"""
        burrow = self.parse_input(simple_input)
        e, pos = burrow.organize()
        self.assertEqual(4446, e)

    def test_sample_least_energy(self):
        amphipod_burrow = self.parse_input(self.sample_input)
        least_energy, pos = amphipod_burrow.organize()
        print(pos)
        self.assertEqual(12521, least_energy)
