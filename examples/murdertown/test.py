import unittest
import sys
from examples.murdertown.cartridge import merge_states

class TestMerge(unittest.TestCase):
    def test_merges_states(self):
        merged_state = merge_states([
            {"a": 1},
            {"b": 2},
            {"c": 3}
        ])
        self.assertEqual(merged_state, {"a": 1, "b": 2, "c": 3})