from unittest import TestCase

from src.resolver import permutations_possibles, replace_zeros_with_list_of_possibilities, replace_list_of_possibilities_whit_0


class Test(TestCase):
    def test_permutations_possible(self):
        results = permutations_possibles(3)
        self.assertTrue(type(results) is list)
        self.assertEqual(results, [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)])

    def test_replace_zeros_with_list_of_possibilities(self):
        results = replace_zeros_with_list_of_possibilities([0, 1, 2, 0], ['x'])
        self.assertEqual(results, [['x'], 1, 2, ['x']])

    def test_replace_list_of_possibilities_whit_0(self):
        results = replace_list_of_possibilities_whit_0([0, [1, 2], 3])
        self.assertEqual(results,[0, 0, 3])