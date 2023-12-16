import unittest
import sys
from examples.murdertown.cartridge import merge_states, BackForwardState, CherryPicker, Map, EvidenceLocker

class TestMerge(unittest.TestCase):
    def test_merges_states(self):
        merged_state = merge_states([
            {"a": 1},
            {"b": 2},
            {"c": 3}
        ])
        self.assertEqual(merged_state, {"a": 1, "b": 2, "c": 3})

    def test_cherrypick_events(self):
        cherrypicker = CherryPicker("mycherrypicker", "previous_state", "says lets go back", "cherrypicker", [
            {"target": "a", "if_the_user": "says a"},
            {"target": "b", "if_the_user": "says b"}
        ])

        state_definition = cherrypicker.dict()
        # Check that state_definition has the key mycherrypicker_previous_state
        self.assertTrue("mycherrypicker_previous_state" in state_definition)
        rest_of_definition = state_definition["mycherrypicker_previous_state"]

        self.assertEqual(rest_of_definition["prompt"], "cherrypicker")
        self.assertEqual(rest_of_definition["events"][0]["target"], "previous_state")
        self.assertEqual(rest_of_definition["events"][0]["if_the_user"], "says lets go back")
        self.assertEqual(rest_of_definition["events"][1]["target"], "a")
        self.assertEqual(rest_of_definition["events"][1]["if_the_user"], "says a")
        self.assertEqual(rest_of_definition["events"][2]["target"], "b")
        self.assertEqual(rest_of_definition["events"][2]["if_the_user"], "says b")