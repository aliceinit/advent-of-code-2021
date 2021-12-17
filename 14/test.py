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
        expand_polymer((polymer, insertion_rules))
        self.assertEqual("NCNBCHB", str(polymer))

        expand_polymer((polymer, insertion_rules))
        self.assertEqual("NBCCNBBBCBHCB", str(polymer))

    def test_build_expansion_table(self):
        _, insertion_rules = self.parse_input(self.sample_input)
        new_rules = expand_rules(insertion_rules, 5)

        self.assertIsInstance(new_rules["NN"], PolymerElement)
        for pair, expansion in new_rules.items():
            print(f"{pair}: {expansion}")
            self.assertEqual(31, len(str(expansion)), f"Wrong result length for pair '{pair}'")

    def test_count_chars(self):
        polymer = Polymer("ABBCCCD")
        counts = polymer.get_letter_counts()
        self.assertEqual({"A": 1, "D": 1, "B": 2, "C": 3}, counts)

    def test_drop_final_char(self):
        polymer = Polymer("ABCD")
        self.assertEqual("ABCD", str(polymer))
        polymer.drop_final_character()
        self.assertEqual("ABC", str(polymer))

    def test_insert_string_between(self):
        pair = Polymer("AB")
        insert_between(pair, pair.next, "CDE")
        self.assertEqual("ACDEB", str(pair))

    def test_insert_polymer_between(self):
        pair = Polymer("AB")
        inner = Polymer("CDE")
        insert_between(pair, pair.next, inner)
        self.assertEqual("ACDEB", str(pair))

    def test_most_and_least_common_elements(self):
        polymer, insertion_rules = self.parse_input(self.sample_input)
        most_common_element, most_common_count, least_common_element, least_common_count = \
            find_most_and_least_common_elements(polymer, insertion_rules, 10)
        self.assertEqual("B", most_common_element)
        self.assertEqual("H", least_common_element)
        self.assertEqual(1749, most_common_count)
        self.assertEqual(161, least_common_count)
        self.assertEqual(1588, most_common_count - least_common_count)

    # def test_most_and_least_common_elements_at_40(self):
    #     polymer, insertion_rules = self.parse_input(self.sample_input)
    #     most_common_element, most_common_count, least_common_element, least_common_count = \
    #         find_most_and_least_common_elements(polymer, insertion_rules, 40)
    #     assert most_common_element == "B"
    #     assert least_common_element == "H"
    #     assert most_common_count - least_common_count == 2188189693529

    # def test_expansion_table_to_18(self):
    #     _, insertion_rules = self.parse_input(self.sample_input)
    #     build_expansion_table(insertion_rules, 19)
    #
    # def test_expand_to_18(self):
    #     """ Test that we can expand rules to depth 20 with decent speed"""
    #     polymer, insertion_rules = self.parse_input(self.sample_input)
    #     expand_polymer(polymer, insertion_rules, 18)
