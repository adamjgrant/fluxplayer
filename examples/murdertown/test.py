import unittest
import sys
from examples.murdertown.cartridge import merge_states, BackForwardState, CherryPicker, Map, EvidenceLocker, Conversation

class TestMerge(unittest.TestCase):
    def test_merges_states(self):
        merged_state = merge_states([
            {"a": 1},
            {"b": 2},
            {"c": 3}
        ])
        self.assertEqual(merged_state, {"a": 1, "b": 2, "c": 3})

    def test_cherrypick_events(self):
        cherrypicker = CherryPicker("previous_state", "says lets go back", "cherrypicker", [
            {"target": "a", "if_the_user": "says a"},
            {"target": "b", "if_the_user": "says b"}
        ])

        state_definition = cherrypicker.dict()
        self.assertEqual(state_definition["prompt"], "cherrypicker")
        self.assertEqual(state_definition["events"][0]["target"], "previous_state")
        self.assertEqual(state_definition["events"][0]["if_the_user"], "says lets go back")
        self.assertEqual(state_definition["events"][1]["target"], "a")
        self.assertEqual(state_definition["events"][1]["if_the_user"], "says a")
        self.assertEqual(state_definition["events"][2]["target"], "b")
        self.assertEqual(state_definition["events"][2]["if_the_user"], "says b")