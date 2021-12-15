import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input_large = """5483143223
                            2745854711
                            5264556173
                            6141336146
                            6357385478
                            4167524645
                            2176841721
                            6882881134
                            4846848554
                            5283751526"""
    sample_input_small = """11111
                            19991
                            19191
                            19991
                            11111"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return read_octopus_energy(f)

    def test_sample_input_large(self):
        initial_energy = self.parse_input(self.sample_input_large)
        expected_state = self.parse_input("""   0397666866
                                                0749766918
                                                0053976933
                                                0004297822
                                                0004229892
                                                0053222877
                                                0532222966
                                                9322228966
                                                7922286866
                                                6789998766  """)
        self.assertEqual((expected_state, 1656),
                         predict_octopodes(initial_energy, steps=100))

    def test_sample_input_small(self):
        initial_energy = self.parse_input(self.sample_input_small)
        expected_phase_1 = self.parse_input(""" 34543
                                                40004
                                                50005
                                                40004
                                                34543""")
        expected_phase_2 = self.parse_input(""" 45654
                                                51115
                                                61116
                                                51115
                                                45654""")
        result_phase_1, _ = predict_octopodes(initial_energy, steps=1)
        result_phase_2, _ = predict_octopodes(initial_energy, steps=2)
        self.assertEqual(expected_phase_1, result_phase_1)
        self.assertEqual(expected_phase_2, result_phase_2)
