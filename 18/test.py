import io
import re
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_input = """  [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
                        [[[5,[2,8]],4],[5,[[9,9],0]]]
                        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
                        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
                        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
                        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
                        [[[[5,4],[7,7]],8],[[8,3],8]]
                        [[9,3],[[9,9],[6,[4,9]]]]
                        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
                        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_snail_homework(f)

    def test_addition_homework(self):
        homework = self.parse_input(self.sample_input)
        total_sum = snail_sum(homework)
        snail_answer = self.parse_input("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")[0]
        self.assertEqual(total_sum.get_magnitude(), snail_answer.get_magnitude())
        self.assertEqual(4140, total_sum.get_magnitude())

    def test_homework_part_two(self):
        homework = self.parse_input(self.sample_input)
        biggest_sum = find_largest_sum_of_two(homework)
        snail_answer = self.parse_input("[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]")[0]
        self.assertEqual(biggest_sum.get_magnitude(), snail_answer.get_magnitude())
        self.assertEqual(3993, biggest_sum.get_magnitude())

    def test_parse_strings_simple(self):
        s = "[1,2]"
        parsed = self.parse_input(s)[0]

        sn = SnailNumber()
        sn.add_left(SnailNumber(1))
        sn.add_right(SnailNumber(2))

        self.assertEqual(parsed.get_magnitude(), sn.get_magnitude())

    def test_parse_multiple_nestings(self):
        s = "[[1,2],3]"
        parsed = self.parse_input(s)[0]

        sn = SnailNumber()
        sn.add_left(SnailNumber())
        sn.left.add_left(SnailNumber(1))
        sn.left.add_right(SnailNumber(2))
        sn.add_right(SnailNumber(3))

        self.assertEqual(parsed.get_magnitude(), sn.get_magnitude())

    def test_magnitude(self):
        s1 = self.parse_input("[9,1]")[0]
        s2 = self.parse_input("[1,9]")[0]
        s3 = self.parse_input("[[9,1],[1,9]]")[0]
        s4 = self.parse_input("[[1,2],[[3,4],5]]")[0]
        s5 = self.parse_input("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")[0]
        s6 = self.parse_input("[[[[1,1],[2,2]],[3,3]],[4,4]]")[0]
        s7 = self.parse_input("[[[[3,0],[5,3]],[4,4]],[5,5]]")[0]
        s8 = self.parse_input("[[[[5,0],[7,4]],[5,5]],[6,6]]")[0]
        s9 = self.parse_input("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")[0]

        self.assertEqual(29, s1.get_magnitude())
        self.assertEqual(21, s2.get_magnitude())
        self.assertEqual(129, s3.get_magnitude())
        self.assertEqual(143, s4.get_magnitude())
        self.assertEqual(1384, s5.get_magnitude())
        self.assertEqual(445, s6.get_magnitude())
        self.assertEqual(791, s7.get_magnitude())
        self.assertEqual(1137, s8.get_magnitude())
        self.assertEqual(3488, s9.get_magnitude())

    def test_sum_snail_numbers(self):
        sn1 = self.parse_input("[1,2]")[0]
        sn2 = self.parse_input("[[3,4],5]")[0]
        sn3 = self.parse_input("[[1,2],[[3,4],5]]")[0]

        self.assertEqual(sn1.sum(sn2).get_magnitude(), sn3.get_magnitude())

    def test_reduce_explode(self):
        sn1 = self.parse_input("[[[[[9,8],1],2],3],4]")[0]
        sn1.reduce()
        sn1_reduced = self.parse_input("[[[[0,9],2],3],4]")[0]

        self.assertEqual(sn1.get_magnitude(), sn1_reduced.get_magnitude())

        sn2 = self.parse_input("[7,[6,[5,[4,[3,2]]]]]")[0]
        sn2.reduce()
        sn2_reduced = self.parse_input("[7,[6,[5,[7,0]]]]")[0]

        self.assertEqual(sn2.get_magnitude(), sn2_reduced.get_magnitude())

        sn3 = self.parse_input("[[6,[5,[4,[3,2]]]],1]")[0]
        sn3.reduce()
        sn3_reduced = self.parse_input("[[6,[5,[7,0]]],3]")[0]

        self.assertEqual(sn3.get_magnitude(), sn3_reduced.get_magnitude())

    def test_reduce_multi_explode(self):
        sn = self.parse_input("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")[0]
        sn.reduce()
        sn_intermediate = self.parse_input("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")[0]
        sn_intermediate.reduce()
        sn_reduced = self.parse_input("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")[0]

        self.assertEqual(sn.get_magnitude(), sn_intermediate.get_magnitude())
        self.assertEqual(sn.get_magnitude(), sn_reduced.get_magnitude())

    def test_split(self):
        sn = self.parse_input("[1,[2,17]]")[0]
        sn.reduce()
        sn_reduced = self.parse_input("[1,[2,[8,9]]]")[0]
        self.assertEqual(sn.get_magnitude(), sn_reduced.get_magnitude())

    def test_sum(self):
        sn1 = self.parse_input("[[[[4,3],4],4],[7,[[8,4],9]]]")[0]
        sn2 = self.parse_input("[1,1]")[0]
        sn_sum = sn1.sum(sn2)
        sn3 = self.parse_input("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")[0]
        self.assertEqual(sn3.get_magnitude(),
                         sn_sum.get_magnitude())

    def test_total_sum(self):
        nums_1 = self.parse_input("""   [1,1]
                                        [2,2]
                                        [3,3]
                                        [4,4]""")
        answer_1 = self.parse_input("[[[[1,1],[2,2]],[3,3]],[4,4]]")[0]
        total_sum_1 = snail_sum(nums_1)
        self.assertEqual(answer_1.get_magnitude(), total_sum_1.get_magnitude())

        nums_2 = self.parse_input("""   [1,1]
                                        [2,2]
                                        [3,3]
                                        [4,4]
                                        [5,5]""")
        answer_2 = self.parse_input("[[[[3,0],[5,3]],[4,4]],[5,5]]")[0]
        total_sum_2 = snail_sum(nums_2)
        self.assertEqual(answer_2.get_magnitude(), total_sum_2.get_magnitude())

        nums_3 = self.parse_input("""   [1,1]
                                        [2,2]
                                        [3,3]
                                        [4,4]
                                        [5,5]
                                        [6,6]""")
        answer_3 = self.parse_input("[[[[5,0],[7,4]],[5,5]],[6,6]]")[0]
        total_sum_3 = snail_sum(nums_3)
        self.assertEqual(answer_3.get_magnitude(), total_sum_3.get_magnitude())

    def test_partial_homework(self):
        sn1 = self.parse_input("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")[0]
        sn2 = self.parse_input("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")[0]
        answer = self.parse_input("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")[0]
        sn_sum = sn1.sum(sn2)
        self.assertEqual(sn_sum.get_magnitude(), answer.get_magnitude())


    def test_total_sum_big(self):
        nums_big = self.parse_input(""" [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
                                        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
                                        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
                                        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
                                        [7,[5,[[3,8],[1,4]]]]
                                        [[2,[2,2]],[8,[8,1]]]
                                        [2,9]
                                        [1,[[[9,3],9],[[9,0],[0,7]]]]
                                        [[[5,[7,4]],7],1]
                                        [[[[4,2],2],6],[8,7]]""")
        answer_big= self.parse_input("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")[0]
        total_sum_big = snail_sum(nums_big)
        self.assertEqual(answer_big.get_magnitude(), total_sum_big.get_magnitude())
