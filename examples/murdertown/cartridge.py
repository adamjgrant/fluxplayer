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

    def key_dict(self):
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
    def __init__(self, previous_state, map_key, go_back_if_the_user="", prompt="", events_to_pick=[]):
      super().__init__("MAP", previous_state, "asks to go back", prompt, events_to_pick)
      self.prompt = f"""
{prompt}

Remember to show the user this map ![map](https://cdn.everything.io/chatgpt/maura/{map_key}.png)
      """

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
The professor received an email from Maura Murray's account that said she would be gone for a week due to a death in the family the
day before a class was to be held over zoom. The professor also learned that Maura had handed in her homework a day early.
The professor later learned that there was no death in the family and that Maura Murray was missing.
Other than this information this professor only says that Maura Murray was a good student and would be surprised if she ran away.
  """),
  "BUTCH_ATWOOD": Person("Butch Atwood", "Bus driver who saw Maura Murray", """
Butch Atwood was driving a school bus when he saw Maura Murray's car crashed into a snowbank.
He pulled over and asked her if she needed help. She said no and that she already called AAA for roadside assistance.
He knew that was a lie because there was no cell service in that area. He offered to call the police for her but she said no.
He went home and called the police anyway. while he didn't have eyes on Maura or tue car while he called, he did notice several cars pass by. Butch claims she didn't look intoxicated nor injured but was cold and shivering. You can share [this link](https://youtu.be/OfrIJQ5xgJE) to an interview with Atwood
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
  "ANONYMOUS_POLICE_DATA_ANALYST": Person("Anonymous Police Data Analyst", "Data analyst working for the FBI", """
The analyst has gathered evidence from security camera footage and Maura's personal computer.
The first reported contact Murray had with anyone on February 9, the day of her disappearance, was at 1:00 pm, when she emailed her boyfriend: "I love you more stud. I got your messages, 
but honestly, I didn't feel like talking too much of anyone, I promise to call today though. Love you, Maura" She also made a phone call inquiring about 
renting a condominium at the same Bartlett, New Hampshire, condo association with which her family had vacationed in the past. Telephone records indicate 
the call lasted three minutes. At 1:13 pm, Murray called a fellow nursing student for reasons unknown.
On the afternoon of Monday, February 9, at 1:24 pm, Murray emailed a work supervisor of the nursing school faculty that she would be out of town for a week due to a death in her family.
She sent a similar email to her professor at the University of Massachusettes at the same time and after sending in her homework early.
Murray used her personal computer to search MapQuest for directions to the Berkshires and Burlington, Vermont.
At 2:05 pm, Murray called a number which provides recorded information about booking hotels in Stowe, Vermont. The call lasted approximately five minutes. 
At 2:18 pm, she telephoned her boyfriend and left a voice message promising him they would talk later. This call ended after one minute.
At 3:15 PM, there is security camera footage of Maura visiting a local ATM withdrawing $280 which is nearly all of the money she has in the account.
The footage shows she's alone when she arrives and leaves.
Shortly after, there is footage at a nearby liquor store where she purchases $40 of alcohol including Baileys Irish Cream, Kahlúa, vodka, and a box of Franzia wine. She also appears alone.
She called to check her voicemail at 4:37 pm, the last recorded use of her cell phone.
  """
  ),
}

class TranscriptState:
    def __init__(self, setting, prompt, events=[], people=[]):
        self.prompt = prompt
        self.events = events
        self.people = people
        self.setting = setting

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
appears before everything spoken.

e.g. '**Mike Crenshaw**: If there's anyone who knows about that it would be...'

If this is the first time the user is speaking to these individuals, they should just greet the user and Mike like this:

**<person's name>**: Hello, I'm <person's name>.

After people have spoken, Mike will either ask a question himself or if several questions have already been asked, he will remind the user they can either 
ask more questions or proceed to somewhere else.

If you haven't already, briefly narrate the setting with some creative flair on how you describe it: {self.setting}

{self.prompt}

{ "Let the user know the following people are available for questioning:" if len(self.people) > 0 else ""}
{"".join(overviews)}

Remember this information is only revealed by each person and only if the user asks the right questions.

            """,
            "events": self.events
        }

cartridge = {
  "START": {
      "role": "",
      "prompt": """
No matter what the user says, show this message unless you already have: 'The information we present to you is based on real events.
The names of the people involved have not been changed. The events are based on the real life disappearance of Maura Murray in 2004.

It is our hope that by presenting this information in a new way, we can help bring new attention to this case and help find Maura Murray.

You will act as one of two investigators on the case starting on February 10, 2004, the day after Maura's disappearance. Time will then progress gradually
and later in larger increments.

With your partner, you will be able to move around freely in this universe. You can talk to the real life people involved in these events 
visit or revisit repeatedly key locations to gather evidence. Your partner will also help you to ask the right questions and move through
unexplored areas.

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
  "The office of a professor at the University of Massachusettes who prefers to remain anonymous",
  "", 
  [],
  [PEOPLE["ANONYMOUS_PROF"]]
)

CRIME_SCENE_DEFINITION = TranscriptState(
  """
Haverhill, New Hampshire. Morning at the scene of a black 1996 Saturn sedan up against the snowbank along Route 112, also known as Wild Ammonoosuc Road. 
The car is pointed west on the eastbound side of the road. The windshield is cracked and the car appears to have been involved in a collision
  """,
  "", 
  [],
  [PEOPLE["BUTCH_ATWOOD"], PEOPLE["FAITH_WESTMAN"], PEOPLE["CECIL_SMITH"], PEOPLE["JOHN_MONAGHAN"], PEOPLE["JEFF_WILLIAMS"]]
)

UMASS_1_DEFINITION = UMASS_DEFINITION.set_events(
  [{ "target": "CRIME_SCENE_1", "if_the_user": "agrees to go to New Hampshire to see the crime scene" }]
).dict()

CRIME_SCENE_1_DEFINITION = CRIME_SCENE_DEFINITION.set_events(
  [{ "target": "INTRO_TO_MAP", "if_the_user": "agrees with Mike's suggestion to continue to the map" }]
).dict()

CRIME_SCENE_2_DEFINITION = CRIME_SCENE_DEFINITION.set_events(
  [{ "target": "UMASS_2", "if_the_user": "agrees to go to U Mass to talk to about communications" }]
).dict()

UMASS_2_DEFINITION = UMASS_DEFINITION.set_events(
  [{ "target": "INTRO_TO_MAP", "if_the_user": "agrees with Mike's suggestion to continue to the map" }]
).dict()

INTRO_TO_MAP_DEFINITION = TranscriptState(
  "At the same scene, with Mike's map folded out showing key locations",
  """
Mike will show this image to the user:

![map](https://cdn.everything.io/chatgpt/maura/map_map2_fbi_data_lab.png)

And let them know from now on they can always ask to review the map to visit another location
to review evidence or talk to someone. All they have to do is ask.
Mike will mention that there are still more places to visit that are not yet on the map and that
as they visit new places, they will start appearing on the map in case the user wants to return
and gather more information. 

The user's choice now is to go to one of the places on the map or to visit the data lab where
they have pieced together some events leading up to her disappearance.
  """,
  [
    { "target": "DATA_LAB", "if_the_user": "decides to go to the data lab'" },
    { "target": "CRIME_SCENE_START", "if_the_user": "decides to go back to the scene of the wrecked saturn'" },
    { "target": "UMASS_START", "if_the_user": "decides to go back to U Mass'" }
  ],
  []
).dict()

DATA_LAB_DEFINITION = TranscriptState(
  """
A data lab in the FBI New Hampshire office. Briefing room with computer equipment and a large television screen.
  """,
  """
  """,
  [{ "target": "MAP_DATA_LAB", "if_the_user": "agrees to go to the map" }],
  [PEOPLE["ANONYMOUS_POLICE_DATA_ANALYST"]]
).dict()

UMASS_START_DEFINITION = UMASS_DEFINITION.set_events(
  []
).dict()

CRIME_SCENE_START_DEFINITION = CRIME_SCENE_DEFINITION.set_events(
  []
).dict()

cartridge = {
  **cartridge,
  "UMASS_1": UMASS_1_DEFINITION,
  "CRIME_SCENE_1": CRIME_SCENE_1_DEFINITION,
  "CRIME_SCENE_2": CRIME_SCENE_2_DEFINITION,
  "UMASS_2": UMASS_2_DEFINITION,
  "INTRO_TO_MAP": INTRO_TO_MAP_DEFINITION,
  "DATA_LAB": DATA_LAB_DEFINITION,
  "CRIME_SCENE_START": CRIME_SCENE_START_DEFINITION,
  "UMASS_START": UMASS_START_DEFINITION,
  **Map("DATA_LAB", "map_map2_fbi_data_lab").key_dict(),
  **Map("CRIME_SCENE_START", "map_map2_fbi_data_lab").key_dict(),
  **Map("UMASS_START", "map_map2_fbi_data_lab").key_dict(),
}