import unittest
import sys
from examples.find_maura_murray.cartridge import BackForwardState, CherryPicker, Map, EvidenceLocker, cartridge, Image
from examples.find_maura_murray.lib.evidence import Evidence, EvidenceSet, EvidenceTrail, ImageEvidence

class TestMerge(unittest.TestCase):
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
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_1", "UMASS_OFFICE_1", "CAR_WRECK_1", "EVIDENCE_LOCKER_2", "DATA_LAB_1", ".SELF"]))

  def test_backbone_level_1_umass(self):
    events = cartridge["UMASS_OFFICE_1"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_UMASS_OFFICE_1", "EVIDENCE_LOCKER_2", ".SELF"])

    map_events = cartridge["MAP_UMASS_OFFICE_1"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_1", "UMASS_OFFICE_1", "CAR_WRECK_1", "EVIDENCE_LOCKER_2", "UMASS_OFFICE_1", ".SELF"]))

  def test_backbone_level_1_car_wreck(self):
    events = cartridge["CAR_WRECK_1"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_CAR_WRECK_1", "EVIDENCE_LOCKER_2", ".SELF"])

    map_events = cartridge["MAP_CAR_WRECK_1"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_1", "UMASS_OFFICE_1", "CAR_WRECK_1", "EVIDENCE_LOCKER_2", "CAR_WRECK_1", ".SELF"]))

class TestStatesLevel2(unittest.TestCase):
  def test_backbone_level_2_data_lab(self):
    events = cartridge["DATA_LAB_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_DATA_LAB_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_DATA_LAB_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "DATA_LAB_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3", ".SELF"]))

  def test_backbone_level_2_umass(self):
    events = cartridge["UMASS_OFFICE_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_UMASS_OFFICE_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_UMASS_OFFICE_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "UMASS_OFFICE_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3", ".SELF"]))

  def test_backbone_level_2_car_wreck(self):
    events = cartridge["CAR_WRECK_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_CAR_WRECK_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_CAR_WRECK_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "CAR_WRECK_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3", ".SELF"]))

  def test_backbone_level_2_evidence_locker(self):
    events = cartridge["EVIDENCE_LOCKER_2"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(targets, ["MAP_EVIDENCE_LOCKER_2", "VISIT_FRED_3", ".SELF"])

    map_events = cartridge["MAP_EVIDENCE_LOCKER_2"]["events"]
    map_targets = [event["target"] for event in map_events]
    self.assertEqual(sorted(map_targets), sorted(["DATA_LAB_2", "UMASS_OFFICE_2", "CAR_WRECK_2", "EVIDENCE_LOCKER_2", "EVIDENCE_LOCKER_2", "VISIT_FRED_3", ".SELF"]))

class TestStatesPenultimateLevel(unittest.TestCase):
  def test_penultimate_level(self):
    events = cartridge["MAP_CAR_WRECK_10"]["events"]
    targets = [event["target"] for event in events]
    self.assertEqual(sorted(targets), sorted([
      ".SELF",
      "DATA_LAB_10", 
      "UMASS_OFFICE_10", 
      "CAR_WRECK_10", 
      "CAR_WRECK_10", 
      "EVIDENCE_LOCKER_MAP_CAR_WRECK_10_10", 
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

class TestEvidence(unittest.TestCase):
  def test_evidence_trail(self):
    evidence_1 = Evidence(date="date1", time="time1", presentation="presentation1", description="description1")
    evidence_2 = Evidence(date="date2", time="time2", presentation="presentation2", description="description2")
    evidence_set_a = EvidenceSet(evidences=[evidence_1, evidence_2], description="description_a")

    evidence_3 = Evidence(date="date3", time="time3", presentation="presentation3", description="description3")
    evidence_4 = Evidence(date="date4", time="time4", presentation="presentation4", description="description4")
    evidence_set_b = EvidenceSet(evidences=[evidence_3, evidence_4], description="description_b")

    evidence_trail = EvidenceTrail(
      key="EVIDENCE_TRAIL_1", 
      date="date", 
      time="time", 
      presentation="presentation", 
      description="description", 
      evidence_set_objects=[{ "EVIDENCE_SET_A": evidence_set_a }, { "EVIDENCE_SET_B": evidence_set_b }],
      previous_backbone_state="NARRATIVE_BACKBONE_STATE",
      previous_backbone_state_description="<example description of narrative backbone state>"
    )

    key_dict = evidence_trail.key_dict()
    self.maxDiff = None
    if_the_user_esa = (x for x in key_dict["EVIDENCE_TRAIL_1"]["events"] if x["target"] == "EVIDENCE_TRAIL_1_EVIDENCE_SET_A").__next__()["if_the_user"]
    if_the_user_esb = (x for x in key_dict["EVIDENCE_TRAIL_1"]["events"] if x["target"] == "EVIDENCE_TRAIL_1_EVIDENCE_SET_B").__next__()["if_the_user"]

    self.assertEqual(if_the_user_esa, f"wants to see evidence that includes: {evidence_set_a.description}")
    self.assertEqual(if_the_user_esb, f"wants to see evidence that includes: {evidence_set_b.description}")

    self.assertDictEqual(key_dict["EVIDENCE_TRAIL_1"], {
      "prompt": f"""
Let the user know they are now in an area of the evidence locker where they can see the evidence described in the events below.
The user will need to choose either to see an evidence set or to go back to a previous state. 
      """,
      "events": [
        { "target": "EVIDENCE_LOCKER", "if_the_user": "wants to go back or back specifically to the evidence locker" },
        { "target": "NARRATIVE_BACKBONE_STATE", "if_the_user": "wants to go back to <example description of narrative backbone state>" },
        { "target": "EVIDENCE_TRAIL_1_EVIDENCE_SET_A", "if_the_user": f"wants to see evidence that includes: {evidence_set_a.description}" },
        { "target": "EVIDENCE_TRAIL_1_EVIDENCE_SET_B", "if_the_user": f"wants to see evidence that includes: {evidence_set_b.description}" },
      ]
    })

    self.assertDictEqual(key_dict["EVIDENCE_TRAIL_1_EVIDENCE_SET_A"], {
      "prompt": f"""
Let the user know they are now looking at a small set of evidence in the evidence locker for "{evidence_set_a.description}" 
and the evidence is as follows:

{evidence_set_a.presentation}
        """,
      "events": [
        { "target": "EVIDENCE_LOCKER", "if_the_user": "wants to go back or back specifically to the evidence locker" },
        { "target": "EVIDENCE_TRAIL_1", "if_the_user": "wants to go back to the evidence set where they were before but not all the way back to the evidence locker" },
        { "target": "NARRATIVE_BACKBONE_STATE", "if_the_user": "wants to go back to <example description of narrative backbone state>" }
      ]
    })

    self.assertDictEqual(key_dict["EVIDENCE_TRAIL_1_EVIDENCE_SET_B"], {
      "prompt": f"""
Let the user know they are now looking at a small set of evidence in the evidence locker for "{evidence_set_b.description}" 
and the evidence is as follows:

{evidence_set_b.presentation}
        """,
      "events": [
        { "target": "EVIDENCE_LOCKER", "if_the_user": "wants to go back or back specifically to the evidence locker" },
        { "target": "EVIDENCE_TRAIL_1", "if_the_user": "wants to go back to the evidence set where they were before but not all the way back to the evidence locker" },
        { "target": "NARRATIVE_BACKBONE_STATE", "if_the_user": "wants to go back to <example description of narrative backbone state>" }
      ]
    })