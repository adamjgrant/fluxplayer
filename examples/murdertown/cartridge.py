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
        self.description = description
        self.information = information

    def overview(self):
        return f"""
          Name: {self.name}
          Background: {self.description}.
          Here's what you need to know about {self.name}:

          {self.information}
        """

PEOPLE = [
]

class RegularState():
    def init(self, prompt):
        self.prompt = prompt

    def dict(self):
        return {
            "prompt": f"""
              All messages you send back to the user must be written in the style of a transcript where a person's name
              appears before everything spoken, and there is no outside narration. 

              e.g. '**Mike Crenshaw**: If there's anyone who knows about that it would be...'

              {self.prompt}
            """,
            "events": []
        }

cartridge = {
  "START": {
      "role": "",
      "prompt": """
        No matter what the user says, show this message: 'The information contained in
        this story is completely true and this remains an open investigation.

        You will act as one of two investigators on a new case of a missing woman last seen waiting for roadside assistance
        after hitting a guardrail on a one lane road.

        With your partner, you will gather evidence by looking at the crime scene
        and talking to the real life people (witnesses, accused, family) involved in these events.

        Anyone with information about Maura Murray is asked to call the New Hampshire Cold Case Unit at (603) 223-3648 
        or email them at Coldcaseunit@dos.nh.gov.

        Ready to meet your fellow investigator and learn more about this case?'

        If the user wants to know more, you can let them know that all of that can be discussed with
        the investigator and ask them again if they're ready.
      """,
      "events": [
        {
          "target": "MEET_MIKE",
          "if_the_user": "says yes or otherwise agrees to meet their fellow investigator"
        },
        {
          "target": "START",
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
          Let the user know that as Mike, your job will be to help them on how to move through the town, where you can go, 
          and whom you can talk to. Lastly, ask them if they're ready to go to the map room where you'll discuss the details
          of this case and decide on where to finally go out into the town to investigate.
    """,
    "events": [
      {
        "target": "GO_TO_MAP_ROOM",
        "if_the_user": "agrees to go to map room or says they're ready"
      }
    ]
  },
  "MAP": {
    "prompt": "",
    "events": [
        {
            "target": "NORTH_SIDE",
            "if_the_user": ""
        },
        {
            "target": "EAST_SIDE",
            "if_the_user": ""
        },
        {
            "target": "WEST_SIDE",
            "if_the_user": ""
        },
        {
            "target": "SOUTH_SIDE",
            "if_the_user": ""
        }
    ]
  }
}

cartridge = {**cartridge}