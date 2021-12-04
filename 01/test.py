from unittest import TestCase
from .main import count_increasing, sum_batches_of_three


class TestCountIncreasing(TestCase):
    def test_sample_input(self):
        sample_input = [199,
                        200,
                        208,
                        210,
                        200,
                        207,
                        240,
                        269,
                        260,
                        263]
        result = count_increasing(sample_input)
        assert result == 7

    def test_all_increasing(self):
        result = count_increasing([1, 2, 3, 4])
        assert result == 3

    def test_none_increasing(self):
        result = count_increasing([4, 3, 2, 1])
        assert result == 0


class TestSumBatchesOfThree(TestCase):
    def test_sample_input(self):
        sample = [199,
                  200,
                  208,
                  210,
                  200,
                  207]
        result = sum_batches_of_three(sample)
        print(result)
        assert result == [607, 618, 618, 617]
