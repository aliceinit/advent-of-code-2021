import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  NNCB

                        CH -> B
                        HH -> N
                        CB -> H
                        NH -> C
                        HB -> C
                        HC -> B
                        HN -> C
                        NN -> C
                        BH -> H
                        NC -> B
                        NB -> B
                        BN -> B
                        BB -> N
                        BC -> B
                        CC -> N
                        CN -> C"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_polymer_and_rules(f)

    def test_sample_data(self):
        polymer, insertion_rules = self.parse_input(self.sample_input)
        process_insertion_step(polymer, insertion_rules)
        self.assertEqual("NCNBCHB", str(polymer))

        process_insertion_step(polymer, insertion_rules)
        self.assertEqual("NBCCNBBBCBHCB", str(polymer))

    def test_multi_step(self):
        polymer, insertion_rules = self.parse_input(self.sample_input)
        process_polymer_insertions(polymer, insertion_rules, 2)
        self.assertEqual("NBCCNBBBCBHCB", str(polymer))

    def test_single_traversal(self):
        polymer, insertion_rules = self.parse_input(self.sample_input)
        process_insertion_single_traversal(polymer, insertion_rules, 2)
        self.assertEqual("NBCCNBBBCBHCB", str(polymer))

    def test_most_and_least_common_elements(self):
        polymer, insertion_rules = self.parse_input(self.sample_input)
        process_polymer_insertions(polymer, insertion_rules, 10)
        most_common_element, most_common_count, least_common_element, least_common_count = \
            find_most_and_least_common_elements(str(polymer))
        assert most_common_element == "B"
        assert least_common_element == "H"
        assert most_common_count - least_common_count == 1588
