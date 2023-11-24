import unittest

import numpy as np

from earthkit.climate import heuristics


class TestHeuristics(unittest.TestCase):
    def test_growing_degree_days_tas_mean(self):
        tas_mean = np.array([[20, 25, 30], [22, 27, 32]])
        tas_base = 15
        expected_result = np.array([[5, 10, 15], [12, 22, 32]])

        result = heuristics.growing_degree_days(tas_mean=tas_mean, tas_base=tas_base)

        np.testing.assert_array_equal(result, expected_result)

    def test_growing_degree_days_tas_min_max(self):
        tas_min = np.array([[18, 23, 28], [20, 25, 30]])
        tas_max = np.array([[22, 27, 32], [24, 29, 34]])
        tas_base = 15
        expected_result = np.array([[5.0, 10.0, 15.0], [12.0, 22.0, 32.0]])

        result = heuristics.growing_degree_days(tas_min=tas_min, tas_max=tas_max, tas_base=tas_base)

        np.testing.assert_array_equal(result, expected_result)

    def test_growing_degree_days_invalid_input(self):
        with self.assertRaises(AssertionError):
            heuristics.growing_degree_days()

    def test_growing_degree_days_invalid_input_both(self):
        with self.assertRaises(AssertionError):
            heuristics.growing_degree_days(
                tas_mean=np.array([[20, 25, 30]]),
                tas_min=np.array([[18, 23, 28]]),
                tas_max=np.array([[22, 27, 32]]),
            )

    def test_heating_degree_days(self):
        tas_max = np.array([[10, 15, 20], [12, 18, 24]])
        tas_mean = np.array([[5, 10, 15], [8, 15, 20]])
        tas_min = np.array([[2, 8, 12], [6, 12, 18]])
        tas_base = 10
        expected_result = np.array([[5, 0, 0], [1, 0, 0]])

        result = heuristics.heating_degree_days(
            tas_max=tas_max, tas_mean=tas_mean, tas_min=tas_min, tas_base=tas_base
        )

        np.testing.assert_array_equal(result, expected_result)

    def test_cooling_degree_days(self):
        tas_max = np.array([[25, 30, 35], [28, 33, 38]])
        tas_mean = np.array([[20, 25, 30], [22, 28, 34]])
        tas_min = np.array([[15, 20, 25], [18, 23, 28]])
        tas_base = 26
        expected_result = np.array([[0, 1, 4], [0, 2, 8]])

        result = heuristics.cooling_degree_days(
            tas_max=tas_max, tas_mean=tas_mean, tas_min=tas_min, tas_base=tas_base
        )

        np.testing.assert_array_equal(result, expected_result)


if __name__ == "__main__":
    unittest.main()
