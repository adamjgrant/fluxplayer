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
  """),
  "FAITH_WESTMAN": Person("Faith Westman", "Neighbor who saw Maura Murray", """
Faith Westman was at home when she saw Maura Murray's car crashed into a snowbank. She left the office that night around 10 past 7.
When she passed by the Saturn on the side of the road, it was facing the opposite direction and there was a police SUV with
the number '001' on the side of it. It was parked
nose-to-nose with the Saturn. She didn't see any people at all. Her cell phone didn't have reception in the area and it didn't look like an accident to her
so she carried on. When she later reached Beaver pond, she made a personal call which Mike can corroborate with phone records.
Mike can also use this information to show that her arrival was several minutes before the police arrived. Faith doesn't totally trust
the police. She also got a call from the police department later and says it was weird that they were asking specifically if she
was sure that it was 001 that she saw on the police car, not asking anything about Maura Murray
  """),
  "CECIL_SMITH": Person("Cecil Smith", "Police officer who responded to the scene", """
Official reports say Cecil Smith was the first officer to arrive on the scene of Maura's car. He was driving a 4x4 explorer and 
was dispatched to the report of a car accident.
When he arrived, he observed a black Saturn facing the wrong direction but no one was in or around the car. He saw there was
something red splashed on the window and the seat of the vehicle. It looked like wine. He approached Butch Atwood about what he saw
and he said Maura didn't appear hurt or intoxicated and that Maura told Butch he didn't need to call 911 and that she claimed she
already called AAA. He said he actually didn't talk to Butch for very long. He claims he talked to Maura's dad Fred. In that communication
Fred allegedly told Officer Smith flippantly that Maura might have just gotten depressed and 'done the old squaw', and that sometimes when you're depressed you just
go off into the woods, you step off, and you die. This response shocked the officer. In another conversation with Maura's sister Kathleen,
the sister told the officer that Maura probably got in a big fight with her boyfriend Fred, went off into the woods, took a bunch of sleeping
pills and died.
  """),
  "JOHN_MONAGHAN": Person("John Monaghan", "Police officer who responded to the scene", """
On the night of the disappearance, he got a call that Butch was reporting a car accident. He confined his search area to the area
where there were stores and people and searched while driving around, staying in his car. He put together a general service report
to note that he was assisting another department with the search. Later, he pulled the surveillance tapes from three locations that
had surveillance to see if Maura Murray was on them. He didn't find anything.
  """),
  "JEFF_WILLIAMS": Person("Jeff Williams", "Police Chief of Haverhill, New Hampshire.", """
It has been claimed that he was the driver of the 001 police SUV, which he denies, corroborating with
Cecil Smith that he is the driver. He also maintains that he was never at the scene.
"""),
  "KATHLEEN_MURRAY": Person("Kathleen Murray", "Maura Murray's sister", """
"""),
  "FRED_MURRAY": Person("Fred Murray", "Maura Murray's father", """
Fred will agree with Cecil's account that Maura might have gone on a 'squaw walk' but says he just didn't know how to express himself and he
was very upset about Maura going missing.
On a separate occasion when Maura wrecked his car, he claims he was upset but told her 'It's gonna be alright, it's not the worst thing in the world'
He 'knows' she wouldn't have committed suicide.
"""),
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

{ "Let the user know the following people are available for questioning:" if len(self.people) > 0 else ""}
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
  [PEOPLE["BUTCH_ATWOOD"], PEOPLE["FAITH_WESTMAN"]]
)

UMASS_1_DEFINITION = UMASS_DEFINITION.set_events(
  [{ "target": "CRIME_SCENE_1", "if_the_user": "agrees to go to New Hampshire to see the crime scene" }]
).dict()

CRIME_SCENE_1_DEFINITION = CRIME_SCENE_DEFINITION.set_events([]).dict()

CRIME_SCENE_2_DEFINITION = CRIME_SCENE_DEFINITION.set_events(
  [{ "target": "UMASS_2", "if_the_user": "agrees to go to U Mass to talk to about communications" }]
).dict()

UMASS_2_DEFINITION = UMASS_DEFINITION.set_events([]).dict()

INTRO_TO_MAP_DEFINITION = TranscriptState(
  """
Mike will show this image to the user:

![map](https://www.adamgrant.info/flux-player/examples/murdertown/map.png)

And let them know from now on they can always ask to review the map to visit another location
to review evidence or talk to someone. All they have to do is ask.
Mike will mention that there are still more places to visit that are not yet on the map and that
as they visit new places, they will start appearing on the map in case the user wants to return
and gather more information. 

The user's choice now is to go to one of the places on the map or to visit the data lab where
they collected some information from Maura's personal computer.
  """,
  [ ]
).dict()

cartridge = {
  **cartridge,
  "UMASS_1": UMASS_1_DEFINITION,
  "CRIME_SCENE_1": CRIME_SCENE_1_DEFINITION,
  "CRIME_SCENE_2": CRIME_SCENE_2_DEFINITION,
  "UMASS_2": UMASS_2_DEFINITION,
  "INTRO_TO_MAP": INTRO_TO_MAP_DEFINITION,
}