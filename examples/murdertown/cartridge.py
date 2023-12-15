class BackForwardState():
  def __init__(self, previous_state):

class CherryPicker(BackForwardState):
  def __init__(self, previous_state, states_to_pick=[]):
    super().__init__(previous_state)

class Map(CherryPicker):
  def __init__(self, previous_state, states_to_pick=[]):
    super().__init__(previous_state, states_to_pick)

class EvidenceLocker(CherryPicker):
  def __init__(self, previous_state, states_to_pick=[]):
    super().__init__(previous_state, states_to_pick)

class Conversation():
    def __init__(self, namespace):
        self.namespace = namespace

    def dict(self):
        return {
            f"{self.namespace}_QUESTION1": {
                "prompt": """
                  Make sure every message you send is written in the style of a transcript where a person's name
                  appears before everything spoken, and there is no outside narration.
                """,
                "events": [
                    {
                        "target": "QUESTION2",
                        "if_the_user": ""
                    }
                ]
            }
        }


cartridge = {
  "START": {
      "role": "",
      "prompt": """
        No matter what the user says, show this message: 'The information contained in
        this story is completely true and this remains an open investigation.

        You will act as one of two investigators travelling the town, examining evidence
        and talking to the real life people (witnesses, accused, family) involved in these events.

        If you have any information on...please contact the...authorities at...

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

cartridge = {**cartridge, **(Conversation("foo").dict())}

print(cartridge)
