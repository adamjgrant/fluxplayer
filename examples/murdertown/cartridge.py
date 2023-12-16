import copy

def merge_states(states=[]):
  merged_state_object = {}
  for obj in states:
      merged_state_object.update(obj)
  return merged_state_object

class BackForwardState():
    def __init__(self, name="", previous_state="", go_back_if_the_user="asks to go back", prompt=""):
      self.events = [ { "target": previous_state, "if_the_user": go_back_if_the_user } ]
      self.prompt = prompt
      self.name = name
      self.previous_state = previous_state

    def dict(self):
      return {
        f"{self.name}_{self.previous_state}": {
          "prompt": self.prompt,
          "events": self.events
        }
      }

class CherryPicker(BackForwardState):
    def __init__(self, name, previous_state, go_back_if_the_user="", prompt="", events_to_pick=[]):
      super().__init__(name, previous_state, go_back_if_the_user, prompt)
      self.events = self.events + events_to_pick

class Map(CherryPicker):
    def __init__(self, previous_state, go_back_if_the_user="", prompt="", events_to_pick=[]):
      super().__init__("MAP", previous_state, go_back_if_the_user, prompt, events_to_pick)

class EvidenceLocker(CherryPicker):
    def __init__(self, previous_state, go_back_if_the_user="", prompt="", events_to_pick=[]):
      super().__init__("EVIDENCE_LOCKER", previous_state, go_back_if_the_user, prompt, events_to_pick)

class Person():
    def __init__(self, name, bio, information):
        self.name = name
        self.bio = bio 
        self.information = information

    def overview(self):
        return f"""
Name: {self.name}
Background: {self.bio}.
This is the information that {self.name} has and will provide only if asked a question that would reveal it:

{self.information}\n\n
        """

PEOPLE = {
  "ANONYMOUS_PROF": Person("Anonymous professor at U Mass", "Received messages from Maura Murray", """
The professor received an email from Maura Murray's account that said she would be gone for a week due to a death in the family.
He later learned that there was no death in the family and that Maura Murray was missing.
Other than this information this professor only says that Maura Murray was a good student and would be surprised if she ran away.
  """),
  "BUTCH_ATWOOD": Person("Butch Atwood", "Bus driver who saw Maura Murray", """
Butch Atwood was driving a school bus when he saw Maura Murray's car crashed into a snowbank.
He pulled over and asked her if she needed help. She said no and that she already called AAA for roadside assistance.
He knew that was a lie because there was no cell service in that area. He offered to call the police for her but she said no.
He went home and called the police anyway. Butch claims she didn't look intoxicated nor injured.
  """)
}

class TranscriptState:
    def __init__(self, prompt, events=[], people=[]):
        self.prompt = prompt
        self.events = events
        self.people = people

    def set_events(self, events):
        self.events = events + [{
          "target": ".SELF",
          "if_the_user": "does not say they are out of questions or asks to go somewhere else."
        }]
        return self

    def dict(self):
        overviews = list(map(lambda person: person.overview(), self.people)) 
        return {
            "prompt": f"""
All messages you send back to the user must be written in the style of a transcript where a person's name
appears before everything spoken, and there is no outside narration. 

e.g. '**Mike Crenshaw**: If there's anyone who knows about that it would be...'

If this is the first time the user is speaking to these individuals, they should just greet the user and Mike like this:

**<person's name>**: Hello, I'm <person's name>.

{self.prompt}

Let the user know the following people are available for questioning:
{"".join(overviews)}

Remember this information is only revealed by each person and only if the user asks the right questions.

After people have spoken, Mike will either ask a question himself or if several questions have already been asked, he will offer to
go to the next state.
            """,
            "events": self.events
        }

cartridge = {
  "START": {
      "role": "",
      "prompt": """
        No matter what the user says, show this message unless you already have: 'The information contained in
        this story is completely true and this remains an open investigation.

        You will act as one of two investigators on a new case of a missing woman last seen waiting for roadside assistance
        after hitting a guardrail on a one lane road.

        With your partner, you will gather evidence by looking at the crime scene
        and talking to the real life people (witnesses, accused, family) involved in these events.

        Anyone with information about Maura Murray is asked to call the New Hampshire Cold Case Unit at (603) 223-3648 
        or email them at Coldcaseunit@dos.nh.gov.

        Ready to meet your fellow investigator and learn more about this case?'

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
        "target": "UMASS_1",
        "if_the_user": "chooses to go to University of Massachusettes to discuss the communication"
      },
      {
        "target": "CRIME_SCENE_2",
        "if_the_user": "chooses to go to New Hampshire to see the abandoned vehicle"
      }
    ]
  }
}

# A/B B/A Criss-cross
UMASS_DEFINITION = TranscriptState(
  "", 
  [],
  [PEOPLE["ANONYMOUS_PROF"]]
)

CRIME_SCENE_DEFINITION = TranscriptState(
  "", 
  [],
  [PEOPLE["BUTCH_ATWOOD"]]
)

UMASS_1_DEFINITION = UMASS_DEFINITION.set_events(
  [{ "target": "CRIME_SCENE_1", "if_the_user": "agrees to go to New Hampshire to see the crime scene" }]
).dict()

CRIME_SCENE_1_DEFINITION = CRIME_SCENE_DEFINITION.set_events([]).dict()

CRIME_SCENE_2_DEFINITION = CRIME_SCENE_DEFINITION.set_events(
  [{ "target": "UMASS_2", "if_the_user": "agrees to go to U Mass to talk to about communications" }]
).dict()

UMASS_2_DEFINITION = UMASS_DEFINITION.set_events([]).dict()

cartridge = {
  **cartridge,
  "UMASS_1": UMASS_1_DEFINITION,
  "CRIME_SCENE_1": CRIME_SCENE_1_DEFINITION,
  "CRIME_SCENE_2": CRIME_SCENE_2_DEFINITION,
  "UMASS_2": UMASS_2_DEFINITION
}