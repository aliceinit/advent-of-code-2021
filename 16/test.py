from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):
    sample_hex = """D2FE28"""
    sample_binary_str = """110100101111111000101000"""

    def test_hex_to_binary_string(self):
        self.assertEqual(self.sample_binary_str, hex_to_binary_string(self.sample_hex))

    def test_bin_to_packets(self):
        packets = parse_packets(self.sample_binary_str)
        self.assertEqual(len(packets), 1)
        self.assertEqual(6, packets[0].version)
        self.assertEqual(4, packets[0].type_id)
        self.assertEqual(2021, packets[0].value)

    def test_nested_packets_length_type_0(self):
        packets = parse_packets("00111000000000000110111101000101001010010001001000000000")
        self.assertEqual([10, 20], [sp.value for sp in packets[0].sub_packets])

    def test_nested_packets_length_type_1(self):
        packets = parse_packets("11101110000000001101010000001100100000100011000001100000")
        self.assertEqual([1, 2, 3], [sp.value for sp in packets[0].sub_packets])

    def test_compute_sum(self):
        expression = "C200B40A82"
        self.assertEqual(1 + 2, compute_expression(expression))

    def test_compute_product(self):
        expression = "04005AC33890"
        self.assertEqual(6 * 9, compute_expression(expression))

    def test_compute_min(self):
        expression = "880086C3E88112"
        self.assertEqual(7, compute_expression(expression))

    def test_compute_max(self):
        expression = "CE00C43D881120"
        self.assertEqual(9, compute_expression(expression))

    def test_compute_gt(self):
        expression = "D8005AC2A8F0"
        self.assertEqual(1, compute_expression(expression))

    def test_compute_lt(self):
        expression = "F600BC2D8F"
        self.assertEqual(0, compute_expression(expression))

    def test_compute_eq(self):
        expression = "9C005AC2F8F0"
        self.assertEqual(0, compute_expression(expression))

    def test_compute_nested_expression(self):
        expression = "9C0141080250320F1802104A08"
        self.assertEqual(1, compute_expression(expression))