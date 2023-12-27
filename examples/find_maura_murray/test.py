import unittest
import sys
from examples.murdertown.cartridge import merge_states, BackForwardState, CherryPicker, Map, EvidenceLocker, cartridge, Image

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

        state_definition = cherrypicker.key_dict()
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


class TestStates(unittest.TestCase):
  def test_first_level_in_story_column(self):
    events = cartridge["START"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MEET_MIKE", ".SELF"])

  def test_second_level_in_story_column(self):
    events = cartridge["MEET_MIKE"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["UMASS_A", "CAR_WRECK_B"])

  def test_first_level_in_story_fork_a(self):
    events = cartridge["UMASS_A"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["CAR_WRECK_A", ".SELF"])

  def test_first_level_in_story_fork_b(self):
    events = cartridge["CAR_WRECK_B"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["UMASS_B", ".SELF"])

  def test_second_level_in_story_fork_a(self):
    events = cartridge["CAR_WRECK_A"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["INTRO_TO_MAP", ".SELF"])

  def test_second_level_in_story_fork_b(self):
    events = cartridge["UMASS_B"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["INTRO_TO_MAP", ".SELF"])

  def test_intro_to_map(self):
    events = cartridge["INTRO_TO_MAP"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["DATA_LAB_1", "CAR_WRECK_1", "UMASS_OFFICE_1", ".SELF"])

class TestStatesLevel1(unittest.TestCase):
  def test_backbone_level_1_data_lab(self):
    events = cartridge["DATA_LAB_1"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_DATA_LAB_1", "EVIDENCE_LOCKER_2", ".SELF"])

    map_events = cartridge["MAP_DATA_LAB_1"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_1", "UMASS_OFFICE_1", "CAR_WRECK_1", "EVIDENCE_LOCKER_2", "DATA_LAB_1"]))

  def test_backbone_level_1_umass(self):
    events = cartridge["UMASS_OFFICE_1"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_UMASS_OFFICE_1", "EVIDENCE_LOCKER_2", ".SELF"])

    map_events = cartridge["MAP_UMASS_OFFICE_1"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_1", "UMASS_OFFICE_1", "CAR_WRECK_1", "EVIDENCE_LOCKER_2", "UMASS_OFFICE_1"]))

  def test_backbone_level_1_car_wreck(self):
    events = cartridge["CAR_WRECK_1"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_CAR_WRECK_1", "EVIDENCE_LOCKER_2", ".SELF"])

    map_events = cartridge["MAP_CAR_WRECK_1"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_1", "UMASS_OFFICE_1", "CAR_WRECK_1", "EVIDENCE_LOCKER_2", "CAR_WRECK_1"]))

class TestStatesLevel2(unittest.TestCase):
  def test_backbone_level_2_data_lab(self):
    events = cartridge["DATA_LAB_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_DATA_LAB_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_DATA_LAB_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "DATA_LAB_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3"]))

  def test_backbone_level_2_umass(self):
    events = cartridge["UMASS_OFFICE_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_UMASS_OFFICE_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_UMASS_OFFICE_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "UMASS_OFFICE_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3"]))

  def test_backbone_level_2_car_wreck(self):
    events = cartridge["CAR_WRECK_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_CAR_WRECK_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_CAR_WRECK_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "CAR_WRECK_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3"]))

  def test_backbone_level_2_evidence_locker(self):
    events = cartridge["EVIDENCE_LOCKER_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_EVIDENCE_LOCKER_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_EVIDENCE_LOCKER_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "EVIDENCE_LOCKER_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3"]))

class TestStatesPenultimateLevel(unittest.TestCase):
  def test_penultimate_level(self):
    events = cartridge["MAP_CAR_WRECK_10"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(sorted(targets), sorted([
      "DATA_LAB_10", 
      "UMASS_OFFICE_10", 
      "CAR_WRECK_10", 
      "CAR_WRECK_10", 
      "EVIDENCE_LOCKER_10", 
      "VISIT_FRED_10", 
      "SEARCH_FOR_MAURA_10", 
      "POLICE_PRECINCT_10", 
      "WORK_FRIEND_10", 
      "JULIE_MURRAY_10", 
      "MAURA_APARTMENT_10", 
      "RED_TRUCK_WITNESS_10", 
      "FRED_MURRAY_WITH_KNIFE_10",
      "A_FRAME_FINAL"
    ]))

class TestImages(unittest.TestCase):
  def test_image(self):
    image = Image(url="image.png", description="image")
    markdown = image.markdown()
    self.assertEqual(markdown, "![image](https://cdn.everything.io/chatgpt/maura/image.png)\n_image, [Open image in new window](https://cdn.everything.io/chatgpt/maura/image.png)_\n\n")