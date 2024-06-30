from unittest import TestCase

from src.resolver import (permutations_possibles, replace_zeros_with_list_of_possibilities,
                          replace_list_of_possibilities_whit_0, determine_last_line, rotate_lists_of_lists)

# ID:33884
grid = [
    [-1, 2, 1, 2, 4, -1],
    [2, 3, 4, 2, 1, 3],
    [1, 4, 3, 1, 2, 3],
    [3, 1, 2, 4, 3, 2],
    [3, 0, 0, 0, 0, 1],
    [-1, 2, 4, 2, 1, -1],
]


class Test(TestCase):
    def test_permutations_possible(self):
        result = permutations_possibles(3)
        self.assertTrue(type(result) is list)
        self.assertEqual(result, [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)])

    def test_replace_zeros_with_list_of_possibilities(self):
        result: list = replace_zeros_with_list_of_possibilities([0, 1, 2, 0], ['x'])
        self.assertEqual(result, [['x'], 1, 2, ['x']])

    def test_replace_list_of_possibilities_whit_0(self):
        result: list = replace_list_of_possibilities_whit_0([0, [1, 2], 3])
        self.assertEqual(result, [0, 0, 3])

    def test_determine_last_line(self):
        result: list = determine_last_line(grid)
        self.assertEqual(result, [(2, 1, 3, 4)])

    def test_rotate_lists_of_lists(self):
        result = rotate_lists_of_lists(grid)
        self.assertEqual(result, [[-1, 2, 1, 3, 3, -1],
                                  [2, 3, 4, 1, 0, 2],
                                  [1, 4, 3, 2, 0, 4],
                                  [2, 2, 1, 4, 0, 2],
                                  [4, 1, 2, 3, 0, 1],
                                  [-1, 3, 3, 2, 1, -1]])
