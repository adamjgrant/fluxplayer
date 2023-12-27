import copy
from examples.find_maura_murray.lib.people import PEOPLE
from examples.find_maura_murray.lib.image import Image
from examples.find_maura_murray.lib.special_states import TranscriptState, CherryPicker, Map, BackForwardState
from examples.find_maura_murray.lib.evidence import EVIDENCE, EvidenceLocker

class LevelMaker:
  def __init__(self, level=1):
    self.level = level

  def get_backbone_name(self, event):
    target_parts = event["target"].split("_")
    target_parts.pop()
    return "_".join(target_parts)

  def key_dict(self):
    global FINAL_STATES
    LEVELING_EVENTS = [
      { "target": f"CAR_WRECK_{self.level}", "if_the_user": "wants to go to the site of the wreck where Maura disappeared" },
      { "target": f"UMASS_OFFICE_{self.level}", "if_the_user": "wants to go to U Mass" },
      { "target": f"DATA_LAB_{self.level}", "if_the_user": "wants to go to the data lab" },
      { "target": f"EVIDENCE_LOCKER_{self.level}", "if_the_user": "asks to go to the evidence locker" },
      { "target": f"VISIT_FRED_{self.level}", "if_the_user": "wants to go to Fred's house" },
      { "target": f"SEARCH_FOR_MAURA_{self.level}", "if_the_user": "wants to go to the search for Maura near the site of the car crash where Maura disappeared" },
      { "target": f"POLICE_PRECINCT_{self.level}", "if_the_user": "wants to go to the police precinct" },
      { "target": f"WORK_FRIEND_{self.level}", "if_the_user": "wants to go to talk to Maura's work friend" },
      { "target": f"JULIE_MURRAY_{self.level}", "if_the_user": "wants to go to Julie Murray's place" },
      { "target": f"MAURA_APARTMENT_{self.level}", "if_the_user": "wants to go to Maura's apartment" },
      { "target": f"RED_TRUCK_WITNESS_{self.level}", "if_the_user": "wants to go to the Swiftwater general store to talk to the witness who saw the red truck" },
      { "target": f"FRED_MURRAY_WITH_KNIFE_{self.level}", "if_the_user": "wants to go to Fred's house to discuss the knife" }
    ]

    backbone_names = map(self.get_backbone_name, LEVELING_EVENTS[0:self.level+2])

    # The map should have the events at its level of the backbone...
    LEVELING_EVENTS_FOR_MAP = LEVELING_EVENTS[0:self.level+2]

    # And the new event at the next level
    EXTRA_LEVELING_EVENT = LEVELING_EVENTS[self.level+2:self.level+3]
    if len(EXTRA_LEVELING_EVENT) > 0:
      EXTRA_LEVELING_EVENT[0]["target"] = EXTRA_LEVELING_EVENT[0]["target"].replace(f"_{self.level}", f"_{self.level+1}")
    else:
      EXTRA_LEVELING_EVENT = FINAL_STATE_EVENTS[0:1]
    LEVELING_EVENTS_FOR_MAP = LEVELING_EVENTS_FOR_MAP + EXTRA_LEVELING_EVENT

    _dict = {}

    for backbone_name in backbone_names:
      _dict.update({
        f"{backbone_name}_{self.level}": globals()[f"{backbone_name}_DEFINITION"].copy_with_changes(
          events = [{ "target": f"MAP_{backbone_name}_{self.level}", "if_the_user": "wants to go to the map" }] + EXTRA_LEVELING_EVENT,
        ).dict(),
        **Map(f"{backbone_name}_{self.level}", f"map_level_{self.level}").add_events(LEVELING_EVENTS_FOR_MAP).key_dict(),
      })

    return _dict

beginning = {
  "START": {
      "role": "",
      "prompt": f"""
Show this message unless you already have: 

"{EVIDENCE["MAURA_MISSING_POSTER"].presentation} The information we present to you is based on real events.
The names of the people involved have not been changed. The events are based on the real life disappearance of Maura Murray in 2004.

It is our hope that by presenting this information in a new way, we can help bring new attention to this case and help find Maura Murray.

You will act as one of two investigators on the case starting on February 10, 2004, the day after Maura's disappearance. Time will then progress gradually
and later in larger increments.

With your partner, you will be able to move around freely in this universe. You can talk to the real life people involved in these events 
visit or revisit repeatedly key locations to gather evidence. Your partner will also help you to ask the right questions and move through
unexplored areas.

Anyone with information about Maura Murray is asked to call the New Hampshire Cold Case Unit at (603) 223-3648 
or email them at Coldcaseunit@dos.nh.gov.

Ready to meet your fellow investigator and learn more about this case?"

If the user doesn't agree to meet the investigator you can let them know that their questions will be answered later.
then ask them again if they're ready.
      """,
      "events": [
        {
          "target": "MEET_MIKE",
          "if_the_user": "says yes or otherwise agrees to meet their fellow investigator"
        },
        {
          "target": ".SELF",
          "if_the_user": "Indicates they are not ready to proceed."
        }
      ]
  },
  "MEET_MIKE": {
    "prompt": """
          Generate a dall-e image of an official FBI photograph of a male investigator in his 40s.

          From now on, the messages you give back to the user will be transcript style, so anything you write must
          have a person's name in front of it. For now, that only person will be the user's fellow investigator, Mike Crenshaw.

          E.g. '**Mike Crenshaw**: If there's anyone who knows about that it would be...'

          As Mike, introduce yourself to the user and let them know their job will be to extract information by asking questions. 
          Let the user know that as Mike, your job will be to help them on how to move through relevant areas, where you can go, 
          and whom you can talk to. Lastly, ask them if they want to go to the University of Massachusettes to discuss
          unusual communication with someone believed to be missing or to New Hampshire where an abandoned vehicle was found.

          Write this in a creative style the way an investigator would talk to a new partner but do not add any information
          that is not present here. If the user asks you for more information, tell them you are just starting to learn this too
          and don't have any more information to give them yet.
    """,
    "events": [
      {
        "target": "UMASS_A",
        "if_the_user": "chooses to go to University of Massachusettes to discuss the communication"
      },
      {
        "target": "CAR_WRECK_B",
        "if_the_user": "chooses to go to New Hampshire to see the abandoned vehicle"
      }
    ]
  }
}

# TODO provide both an index and the full information from the evidence object using common methods.
EVIDENCE_LOCKER_DEFINITION = TranscriptState(
  setting="A carefully guarded room in the FBI New Hampshire office with lockers containing evidence for different cases",
  prompt="""
  Mike will give the user a list of evidence currently on file and will explain how additional evidence will be gathered
  as they progress to visit more places and talk to more people. He will also explain that they can always ask to go back to
  the map to visit another location to review evidence or talk to someone. All they have to do is ask.
  """,
  events=[
    { "target": "MAP_EVIDENCE_LOCKER", "if_the_user": "asks to go to map" }
  ],
  people=[],
  next_backbone="Murray Family Home"
)

# A/B B/A Criss-cross
UMASS_OFFICE_DEFINITION = TranscriptState(
  "The office of a professor at the University of Massachusettes who prefers to remain anonymous",
  "", 
  [],
  [PEOPLE["ANONYMOUS_PROF"]]
)

CAR_WRECK_DEFINITION = TranscriptState(
  setting = """
Haverhill, New Hampshire. Morning at the scene of a black 1996 Saturn sedan up against the snowbank along Route 112, also known as Wild Ammonoosuc Road. 
The car is pointed west on the eastbound side of the road. The windshield is cracked and the car appears to have been involved in a collision
  """,
  prompt = """
  """,
  events=[],
  people=[PEOPLE["BUTCH_ATWOOD"], PEOPLE["FAITH_WESTMAN"], PEOPLE["CECIL_SMITH"], PEOPLE["JOHN_MONAGHAN"], PEOPLE["JEFF_WILLIAMS"]]
)

UMASS_A_DEFINITION = UMASS_OFFICE_DEFINITION.set_events(
  [{ "target": "CAR_WRECK_A", "if_the_user": "agrees to go to New Hampshire to see the crime scene" }]
).copy_with_changes(prompt="Remind the user at the end of your message they can also go to the site of a car wreck as their next step.").dict()

CAR_WRECK_B_DEFINITION = CAR_WRECK_DEFINITION.set_events(
  [{ "target": "UMASS_B", "if_the_user": "agrees to go to U Mass to talk to about communications" }]
).copy_with_changes(prompt="Remind the user at the end of your message they can also go to the University of Massachusettes as their next step.").dict()

CAR_WRECK_A_DEFINITION = CAR_WRECK_DEFINITION.set_events(
  [{ "target": "INTRO_TO_MAP", "if_the_user": "agrees with Mike's suggestion to continue to the map" }]
).copy_with_changes(prompt="Remind the user at the end of your message they can also view a map of other locations to visit as their next step.").dict()

UMASS_B_DEFINITION = UMASS_OFFICE_DEFINITION.set_events(
  [{ "target": "INTRO_TO_MAP", "if_the_user": "agrees with Mike's suggestion to continue to the map" }]
).copy_with_changes(prompt="Remind the user at the end of your message they can also view a map of other locations to visit as their next step.").dict()

map_intro_image = Image(url="map_intro.png", description="Map of key locations").markdown()
INTRO_TO_MAP_DEFINITION =TranscriptState(
  "At the same scene, with Mike's map folded out showing key locations",
  f"""
Mike will show this image to the user:

{map_intro_image}

And let them know from now on they can always ask to review the map to visit another location
to review evidence or talk to someone. All they have to do is ask.
Mike will mention that there are still more places to visit that are not yet on the map and that
as they visit new places, they will start appearing on the map in case the user wants to return
and gather more information. 

The user's choice now is to go to one of the places on the map or to visit the data lab where
they have pieced together some events leading up to her disappearance.
  """,
  [
    { "target": "DATA_LAB_1", "if_the_user": "decides to go to the data lab'" },
    { "target": "CAR_WRECK_1", "if_the_user": "decides to go back to the scene of the wrecked saturn'" },
    { "target": "UMASS_OFFICE_1", "if_the_user": "decides to go back to U Mass'" }
  ],
  [],
  "Data Lab"
).dict()

DATA_LAB_DEFINITION = TranscriptState(
  """
A data lab in the FBI New Hampshire office. Briefing room with computer equipment and a large television screen.
  """,
  """
  """,
  [
    { "target": "MAP_DATA_LAB_1", "if_the_user": "agrees to go to the map" }
  ],
  [PEOPLE["ANONYMOUS_POLICE_DATA_ANALYST"]],
  "Evidence Locker"
)

UMASS_START_DEFINITION = UMASS_OFFICE_DEFINITION.copy_with_changes(
  events = [
    { "target": "MAP_CRIME_SCENE_START", "if_the_user": "wants to go to the scene of the accident where Maura disappeared" }
  ]
)

CRIME_SCENE_START_DEFINITION = CAR_WRECK_DEFINITION.copy_with_changes(
  events = [
    { "target": "MAP_CRIME_SCENE_START", "if_the_user": "wants to go to the map" }
  ],
  people = [
    PEOPLE["BUTCH_ATWOOD"],
    PEOPLE["JOHN_MAROTTE"],
    PEOPLE["FAITH_WESTMAN"],
    PEOPLE["KAREN_MCNAMARA"],
    PEOPLE["ANONYMOUS_FISH_AND_GAME_SEARCH_LEAD"]
  ]
)


VISIT_FRED_DEFINITION = TranscriptState(
  setting = "The home of the Murray family in Hanson Massachusettes on February 10th, 2004 at 10PM. Fred is seated at the dining table alone",
  prompt = """
    Fred recieves a voicemail on his home answering machine earlier in the day at 2:30PM stating that Maura's car was found
    abandoned. He was working out of state and had not received the call. Then Maura's other sister Kathleen called him at 5PM
    informing him that Maura was missing. Fred immediately called the Haverhill police department and was told that if Maura was not reported
    safe by the following morning, the New Hampshire Fish and Game department would start a search. Maura was only referred to as missing
    by the department at 5:17PM.
  """,
  events = [],
  people = [PEOPLE["FRED_MURRAY"]],
  next_backbone = "Search party for Maura"
)

SEARCH_FOR_MAURA_DEFINITION = TranscriptState(
  setting = "Dawn in Haverhill, New Hampshire at the hairpin turn at Route 112",
  prompt = """
    There are no footprints on the ground from the scene of the wreck. Helicopters, officers, volunteers, and a canine team
    canvas the area. They are also checking local motels, handing out flyers
  """,
  events = [],
  people = [
    PEOPLE["FRED_MURRAY"], 
    PEOPLE["ANONYMOUS_FISH_AND_GAME_SEARCH_LEAD"],
    PEOPLE["BUTCH_ATWOOD"],
    PEOPLE["JOHN_MAROTTE"],
    PEOPLE["FAITH_WESTMAN"],
    PEOPLE["KAREN_MCNAMARA"],
    PEOPLE["CECIL_SMITH"],
    PEOPLE["JOHN_MONAGHAN"],
    PEOPLE["JEFF_WILLIAMS"]
  ],
  next_backbone = "Police Precinct"
)

POLICE_PRECINCT_DEFINITION = TranscriptState(
  setting = "The office of an anonyous investigator at a police precinct near the University of Massachusettes at Amherst",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["ANONYMOUS_INVESTIGATOR"]],
  next_backbone = "Murray house where a work friend of Maura's is seated with Fred"
)

WORK_FRIEND_DEFINITION = TranscriptState(
  setting = "Back at the Murray household where now Fred and an anonymous work friend of Maura's are seated in the living room.",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["ANONYMOUS_WORK_FRIEND"], PEOPLE["FRED_MURRAY_2"], PEOPLE["BILLY"]],
  next_backbone = "A café where Julie Murray is ready to speak to us"
)

JULIE_MURRAY_DEFINITION = TranscriptState(
  setting = "A local coffee shop in Hanson Massachusettes where Julie Murray is seated with a coffee.",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["JULIE_MURRAY"]],
  next_backbone = "Maura's apartment"
)

MAURA_APARTMENT_DEFINITION = TranscriptState(
  setting = "Maura's apartment with her landlord. A Haverhill police officer is also there with items found in Maura's car",
  prompt = """
    Maura's things are all in boxes. It is unclear if she packed those boxes before leaving or if she just never unpacked them
    before moving in.
    There were also reports of a letter left in the dorm room addressed to Billy.
  """,
  events = [],
  people = [PEOPLE["ANONYMOUS_HAVERHILL_OFFICER"], PEOPLE["BILLY"]],
  next_backbone = "Swiftwater General Store"
)

RED_TRUCK_WITNESS_DEFINITION = TranscriptState(
  setting = "Haverhill Swiftwater General Store where a witness waits outside to talk with Mike and the user",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["RED_TRUCK_WITNESS"]],
  next_backbone = "Murray residence again where Fred has reported receiving a bloody knife."
)

FRED_MURRAY_WITH_KNIFE_DEFINITION = TranscriptState(
  setting = "December 8, 2004. The Murray family house. Fred, Julie, and Kathleen Murray are all seated in the living room",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["FRED_MURRAY_3"], PEOPLE["JULIE_MURRAY"], PEOPLE["KATHLEEN_MURRAY"]],
  next_backbone = "A-frame house"
)

FINAL_STATES = [
  ["A_FRAME_FINAL", "A-Frame"],
  ["U_MASS_FINAL", "U Mass"],
  ["CRIME_SCENE_FINAL", "scene of the car wreck where Maura disappeared"],
  ["DATA_LAB_FINAL", "data lab"],
  ["MURRAY_RESIDENCE_FINAL", "Murray family residence"],
  ["POLICE_PRECINCT_FINAL", "Massachusettes police precinct"],
  ["MAURA_APARTMENT_FINAL", "apartment where Maura was living"],
  ["RED_TRUCK_WITNESS_FINAL", "Swiftwater general store where the red truck was witnessed"]
]
FINAL_STATE_EVENTS = []
for tuple in FINAL_STATES:
  FINAL_STATE_EVENTS = FINAL_STATE_EVENTS + [{
    "target": tuple[0],
    "if_the_user": f"asks to go to the {tuple[1]}"
  }]

FINAL_MAP_EL_EVENTS = [{
  "target": "MAP_EVIDENCE_LOCKER",
  "if_the_user": "asks to go to the map"
}, {
  "target": "EVIDENCE_LOCKER_MAP",
  "if_the_user": "asks to go to the evidence_locker"
}]

cartridge = {
  # Introduction to story
  **beginning,

  # Choices to go to either UMass or the crime scene
  "UMASS_A": UMASS_A_DEFINITION,
  "CAR_WRECK_B": CAR_WRECK_B_DEFINITION,

  # Same choices in an alternate order
  "CAR_WRECK_A": CAR_WRECK_A_DEFINITION,
  "UMASS_B": UMASS_B_DEFINITION,

  # Introduced to the map where they can revisit those two places.
  "INTRO_TO_MAP": INTRO_TO_MAP_DEFINITION,

  ##############################
  # NARRATIVE BACKBONE LEVEL 1 #
  ##############################

  # Adds DATA LAB
  **LevelMaker(1).key_dict(),

  # Continuing the backbone from the data lab, the next state is an introduction
  # to the evidence locker where they can review evidence they've gathered
  # Similar to the dummy non-reversible intro to map, this will also be a dummy
  # but those going forwards won't be.

  ##############################
  # NARRATIVE BACKBONE LEVEL 2 #
  ##############################

  # Adds EVIDENCE_LOCKER
  **LevelMaker(2).key_dict(),
  
  ##############################
  # NARRATIVE BACKBONE LEVEL 3 #
  ##############################

  # From this state, they can go to the next part of the narrative backbone
  # which is to advance the day to February 10th and visit Fred. 

  # Adds VISIT_FRED
  **LevelMaker(3).key_dict(),

  ##############################
  # NARRATIVE BACKBONE LEVEL 4 #
  ##############################

  # Then, dawn the next day where a ground and air search begins. A dog search leads
  # Maura's scent 100 yards east until it stops. Here we also reveal the unaccounted hour of driving time.

  # Adds SEARCH_FOR_MAURA
  **LevelMaker(4).key_dict(),

  ##############################
  # NARRATIVE BACKBONE LEVEL 5 #
  ##############################

  # Then, a talk with a police officer who was involved in an arrest of Maura two
  # a few months earlier for Credit Card fraud.
  
  # Adds POLICE_PRECINCT
  **LevelMaker(5).key_dict(),

  ##############################
  # NARRATIVE BACKBONE LEVEL 6 #
  ##############################

  # Then, we'll talk to a work friend of hers visiting Fred's place who can both tell the story both of her going
  # car shopping, then borrowing dad's car, then going to the party and having to
  # get back in an inexplicable hurry. This can also cover the call from the sister since it happened
  # at work and this is a work friend.

  # Adds WORK_FRIEND
  **LevelMaker(6).key_dict(),

  ##############################
  # NARRATIVE BACKBONE LEVEL 7 #
  ##############################

  # Then, we go to Julie's place where we can cover the boyfriend Billy.
  # This can also bring up the strange voicemail Billy got

  # Adds JULIE_MURRAY
  **LevelMaker(7).key_dict(),

  ##############################
  # NARRATIVE BACKBONE LEVEL 8 #
  ##############################

  # Then, we go to Maura's apartment where there is the directions to Burlington VT and a book about
  # Hiking accidents

  # Adds MAURA_APARTMENT
  **LevelMaker(8).key_dict(),

  ##############################
  # NARRATIVE BACKBONE LEVEL 9 #
  ##############################

  # Then, the witness who saw the red truck at the general store.

  # Adds RED_TRUCK_WITNESS
  **LevelMaker(9).key_dict(),

  ###############################
  # NARRATIVE BACKBONE LEVEL 10 #
  ###############################

  # Then, we go back to Fred's where he has received the rusted stained knife.

  # Adds FRED_MURRAY_WITH_KNIFE
  **LevelMaker(10).key_dict(),

  #####################################
  # NARRATIVE BACKBONE LEVEL 11 FINAL #
  #####################################

  # Then, the A-frame. The final state where they can actually move freely to all nodes.
  "A_FRAME_FINAL": TranscriptState(
    setting = "October 4, 2006. An A-Frame house approximately 1 mile from the crash site, nestled in the woods.",
    prompt = """
    """,
    events = FINAL_MAP_EL_EVENTS,
    people = [PEOPLE["TRUTH_SEEKER"]]
  ).dict(),

  **Map(
        previous_state = "EVIDENCE_LOCKER",
        map_key = "map_level_final"
      ).hard_set_events(FINAL_STATE_EVENTS + [
        {
          "target": "EVIDENCE_LOCKER_MAP",
          "if_the_user": "Wants to go to the evidence locker"
        }
      ]).key_dict(),

  **EvidenceLocker(
        previous_state="MAP",
        level="FINAL",
      ).hard_set_events([
        {
          "target": "MAP_EVIDENCE_LOCKER",
          "if_the_user": "Wants to go to the map"
        }
      ]).key_dict(),

  # The rest of these nodes are copies (where needed) to permanently put the individuals in places
  # where the user can move to and interview. So the map is basically the central node for now.
  "U_MASS_FINAL": UMASS_OFFICE_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS).dict(),
  "CRIME_SCENE_FINAL": CAR_WRECK_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS,
    people = [
      PEOPLE["BUTCH_ATWOOD"],
      PEOPLE["JOHN_MAROTTE"],
      PEOPLE["FAITH_WESTMAN"],
      PEOPLE["KAREN_MCNAMARA"],
      PEOPLE["ANONYMOUS_FISH_AND_GAME_SEARCH_LEAD"]
    ]
  ).dict(),
  "DATA_LAB_FINAL": DATA_LAB_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS).dict(),
  "MURRAY_RESIDENCE_FINAL": TranscriptState(
    setting = "The Murray family home living room, present day.",
    people = [
      PEOPLE["FRED_MURRAY"],
      PEOPLE["KATHLEEN_MURRAY"],
      PEOPLE["JULIE_MURRAY"],
      PEOPLE["BILLY"],
      PEOPLE["ANONYMOUS_WORK_FRIEND"]
    ],
    events = FINAL_MAP_EL_EVENTS
  ).dict(),
  "POLICE_PRECINCT_FINAL": POLICE_PRECINCT_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS,
    people = [
      PEOPLE["CECIL_SMITH"],
      PEOPLE["JOHN_MONAGHAN"],
      PEOPLE["JEFF_WILLIAMS"],
      PEOPLE["ANONYMOUS_INVESTIGATOR"]
    ] 
  ).dict(),

  "MAURA_APARTMENT_FINAL": MAURA_APARTMENT_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS).dict(),
  "RED_TRUCK_WITNESS_FINAL": RED_TRUCK_WITNESS_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS).dict()
}

# Print out each key in the object
debug_states_to_and_from = False

if debug_states_to_and_from:
  for key in cartridge:
    print(key)
    for event in cartridge[key]["events"]:
      print(f"    {event['target']}")
    print("\n")