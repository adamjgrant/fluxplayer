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

    def add_events(self, events=[]):
      self.events = self.events + events

    def state_name(self):
      return f"{self.name}_{self.previous_state}"

    def key_dict(self):
      obj = {}
      state_name = self.state_name()
      obj[state_name] = {
          "prompt": self.prompt,
          "events": self.events
        }
      return obj

    def hard_set_events(self, events):
      self.events = events
      return self

class CherryPicker(BackForwardState):
    def __init__(self, name, previous_state="_", go_back_if_the_user="", prompt="", events_to_pick=[]):
      super().__init__(name, previous_state, go_back_if_the_user, prompt)
      self.events = self.events + events_to_pick

class Map(CherryPicker):
    def __init__(self, previous_state, map_key, go_back_if_the_user="", prompt="", events_to_pick=[]):
      super().__init__("MAP", previous_state, "asks to go back", prompt, events_to_pick)
      self.map_key = map_key
      self.events_to_pick = events_to_pick
      self.prompt = f"""
{prompt}

Remember to show the user this map ![map](https://cdn.everything.io/chatgpt/maura/{map_key}.png)
      """

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

    def copy_with_new_information(self, information):
        person = Person(
          name = self.name,
          bio = self.bio,
          information = f"{self.information}\n{information}"
        )
        return person

PEOPLE = {
  "ANONYMOUS_PROF": Person("Anonymous professor at U Mass", "Received messages from Maura Murray", """
The professor received an email from Maura Murray's account that said she would be gone for a week due to a death in the family the
day before a class was to be held over zoom. The professor also learned that Maura had handed in her homework a day early.
The professor later learned that there was no death in the family and that Maura Murray was missing.
Other than this information this professor only says that Maura Murray was a good student and would be surprised if she ran away.
  """),
  "BUTCH_ATWOOD": Person("Butch Atwood", "Bus driver who saw Maura Murray", """
Butch Atwood was driving a school bus when he saw Maura Murray's car crashed into a snowbank. He lives just 100 yards away from the scene.
He pulled over and asked her if she needed help. She said no and that she already called AAA for roadside assistance.
He knew that was a lie because there was no cell service in that area. He offered to call the police for her but she said no.
He went home and called the police anyway. while he didn't have eyes on Maura or tue car while he called, he did notice several cars pass by. Butch claims she didn't look intoxicated nor injured but was cold and shivering. You can share [this link](https://youtu.be/OfrIJQ5xgJE) to an interview with Atwood
  """),
  "JOHN_MAROTTE": Person("John Marotte", "Neighbor who saw activity around Maura's car", """
With his wife Virginia, John saw someone walking around Maura's car and spending some time near the trunk. Other than that, they didn't
witness anything else.
  """),
  "FAITH_WESTMAN": Person("Faith Westman", "Neighbor who saw Maura Murray", """
Faith Westman was at home when Maura Murray's car crashed into a snowbank. Her house was the closest to the accident. She heard a loud 
thud and saw a single-car accident.
From her point of view, it looked like a car had gone over the curb on a hairpin turn and crashed into a snowbank.
She told police she saw a man in the vehicle smoking a cigarette.
  """),
  "KAREN_MCNAMARA": Person("Karen McNamara", "Neighbor who saw a car parked in front of Maura's", """
She left the office that night around 10 past 7 and arrived at the scene around 7:37 pm.
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
Later when EMS arrived, he joined Butch Atwood to search the area west around the accident. They don't find Maura or even foot prints.
Some of Maura's personal belongings were scattered inside, but her cell phone, credit cards, and backpack are all gone. Inside the card he finds an open 
coke bottle filled with a red liquid that smelled of alcohol. 
  """),
  "JOHN_MONAGHAN": Person("John Monaghan", "Police officer who responded to the scene", """
On the night of the disappearance, he got a call that Butch was reporting a car accident. He confined his search area to the area
where there were stores and people and searched while driving around, staying in his car. He put together a general service report
to note that he was assisting another department with the search. Later, he pulled the surveillance tapes from three locations that
had surveillance to see if Maura Murray was on them. He didn't find anything.
  """),
  "JEFF_WILLIAMS": Person("Chief Jeff Williams", "Police Chief of Haverhill, New Hampshire.", """
It has been claimed that he was the driver of the 001 police SUV, which he denies, corroborating with
Cecil Smith that he is the driver. He also maintains that he was never at the scene.
Separately and after the Murray incident, the Chief was arrested and charged for driving while intoxicated and disobeying orders.
While getting pulled over for speeding, he drunkenly tried to get away by driving even faster while his own officers pursued him.
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
  "BILLY": Person("Billy Rausch", "Boyfriend of Maura Murray", """
    Billy met Maura at Westpoint Military Academy in upstate NY during Maura's sophomore year and transferred to U Mass shortly after to study Nursing.
    At this point, they were dating long distance through the point of her disappearance. Maura planned on spending time in Oklahoma where he was stationed.
    Billy will describe their relationship as "engaged to be engaged".
    Billy says he received a voicemail from Maura the day after Maura disappeared, Billy turned off his cellphone as he boarded a plane
    to assist in the search efforts. Shortly after he did, he received a voicemail from an unknown number. It was short and wordless. He says
    He could only hear crying and at the end a whimper. He swears this was Maura. Officials traced the number to an AT&T calling card. He remembers
    this well because Billy's mother Sharon gave Maura two AT&T calling cards a couple months earlier. Haverhill police claimed they traced the call
    back to the American Red cross. Yet Sharon says multiple private investigators had tried and failed to trace the call.
    Billy is also aware of the claim of a letter left in Maura's dorm room addressed to him. However he says he was with the officers when the dorm
    room was being searched and there was no letter. It's not clear where this information came from.
  """),
  "JULIE_MURRAY": Person("Julie Murray", "Maura Murray's second oldest sister", """
    Julie attended West Point at the same time as Maura and ran track together and were incredibly close.
    Julie and Billy weren't close but they shared some friends. Julie caught wind of a rumor that Billy might be cheating on Maura.
    She confronted Maura about it, expressing her concerns as a big sister and suggested it was time for Maura to move on. She will say
    Maura and Billy got into fights fairly frequently. When they did, Maura needed to be comforted and talked down afterwards.
  """),
  "KATHLEEN_MURRAY": Person("Kathleen Murray", "Maura Murray's oldest sister", """
    On February 5, 2004, Kathleen got out of rehab and her boyfriend celebrated by taking her to a liquor store. After relapsing mixing sleeping pills with alcohol,
    Kathleen made a troubling call to Maura but is not able to divulge further details on what they discussed. 
  """),
  "ANONYMOUS_INVESTIGATOR": Person("A Massachusettes Police Department investigator", "Worked on a previous case involving Maura Murray prior to her disappearance", """
    A few months before Maura's disappearance, The investigator worked on a case where someone has been using a stolen credit card to order
    food delivered to a U Mass dormitory. They were able to set up a sting operation by waiting for the same individual to order pizza. When they did,
    the investigator travelled with the delivery person to the dormitory. Maura Murray came to pick up the order. She was tried and convicted for the crime.
    She was very cooperative and scared when she was confronted. The judge dropped the charges contingent on three months of good behavior.
  """),
  "ANONYMOUS_WORK_FRIEND": Person("Anonymous Work Friend", "A friend of Maura's who also works shifts with her", """
    On the same weekend night when Maura dropped off Fred at the Quality Inn and borrowed his Toyota Corolla, Maura attended a dorm party
    with friends in the evening. The friend doesn't know much about what happened at the party but they found it strange that later into the evening, 
    Maura said she needed to get the car back to her father. Now that they and Fred have exchanged these details, they both find it odd given
    that it would have been fine if she came back the next day with the car. He wasn't expecting it that evening. She had also been drinking
    so she could have sobered up over the evening. The friend feels like she had another reason for leaving such as leaving for or from something.

    On another occasion prior to this on February 5, 2004, the friend and Maura were at work together. During the shift, Maura received a phone
    call that made her so upset, she just stares out the window completely disengaged. Her supervisor was so worried for her, he ends her shift
    early and walks her back to her dorm room. When the friend asks what's wrong, the only thing she says is "my sister."
  """),
  "RED_TRUCK_WITNESS": Person("Anonymous Red Truck Witness", "", """
    On the night Maura went missing, this woman was walking to the Swiftwater general store, a red truck passed by her and slowed down
    for some reason. It was too dark to see the passengers. As she got closer, it took off up the hill and out of sight. She saw it again soon
    after soon after idling outside the general store. When she stepped out into the light of the parking lot, the car sped off down
    the road in the direction of Maura's accident. They went inside and asked about the truck. They said, no one came in. It wasn't long until
    a police cruiser and ambulance came by heading in the same direction. The only way she can describe the truck is that it looked like
    someone who was delivering wood.
  """),
  "TRUTH_SEEKER": Person("", "", """
    This individual is aware of a previous search of the A-frame house with Fred and volunteers and the person who implicated his brother.
    They came with cadaver dogs which became active around a closet upstairs indicating human remains might have been there. Private investigators
    cut out two pieces of the carpet in the closet. They sent one to New Hampshire police but heard nothing back. Then in 2016, private investigators
    returned to the A-frame house and notice stains on the walls of the closet. They were able to confirm with testing the stains are the blood of two
    people. One person was male, the other person was inconclusive and could not be confirmed to belong to Maura due to the sample size and
    degredation of the blood.
  """),
  "ANONYMOUS_HAVERHILL_OFFICER": Person("Anonymous Haverhill Officer", "Officer who searched Maura's car, providing the items found", """
    The officer found a computer printout of directions to Burlington, VT and a copy of a book about hiking accidents in New Hampshire.
    He also found a box of Franzia wine, an open coke bottle filled with a red liquid that smelled of alcohol. Her cellphone, credit cards, and backpack
    were all gone.
  """),
  "ANONYMOUS_FISH_AND_GAME_SEARCH_LEAD": Person("Anonymous Fish & Game Search Lead", "", """
    The team this person lead canvassed the area handing out flyers and checking with local motels. They used a leather glove belonging to Maura
    to train the canine team to Maura's scent. The canines were able to trace Maura's scent up the road about 100 yards east of the accident where it
    abruptly stopped. By nightfall, no other significant evidence was found in a 2 mile radius.
  """)
}

PEOPLE["FRED_MURRAY_2"] = PEOPLE["FRED_MURRAY"].copy_with_new_information("""
  The weekend before Maura went missing, Fred visited Maura at U Mass to go car shopping with her. He knew her 1996 Saturn was breaking down and was
  desperately in need of a new one. They spent Saturday afternoon missing but didn't buy anything. In the evening, Fred offered to let Maura use his
  car for the evening. She accepts, drops him off at a Quality inn where he's staying and heads back to campus.
  Later that evening, Maura crashed the Toyota Corolla into a guard rail causing $10,000 of damage to the car. The police went to the scene
  but there were no charges against Maura and a breathalizer was not administered. The police drove Maura back to the Quality Inn to stay
  with her dad.
  The following day, Fred finds out that insurance is going to cover the damage. However before filing the claim, he asks Maura to pick up
  accident forms at the Registry of Motor Vehicles. Fred goes back home to Massachusettes and called her later at 11:30PM to remind her to get it
  done. They make a plan to go over the forms the following night. This never happened because it's the night Maura disappeared.
  Fred believes Maura was most likely headed to Bartlett, New Hampshire on the night of her disappearance. Growing up, the Murrays used to go
  hiking frequently, as often as four times a week. She loved the white mountains.
""")

PEOPLE["FRED_MURRAY_3"] = PEOPLE["FRED_MURRAY"].copy_with_new_information("""
  In late 2004, a stranger approached Fred with a rusted and reddish-brown stained knife and tells him "I think my brother might have killed your daughter."
  The stranger's brother lived in an A-Frame house less than a mile from the crash. After that night, he remembered his brother acting
  really strange. Later he found a bloody knife in the glove compartment of his brother's car. Fred mails the knife to New Hampshire police along
  with a note explaining everything. Fred gets a confirmation letter days later confirming they've received the package. Fred never heard
  anything else about it or learned of any other lab results. He also found out that a backpack possibly belonging to Maura was found in the woods
  but didn't know anything else about it. Officials on the case have only responded, "we are aware of the backpack."
""")

class TranscriptState:
    def __init__(self, setting, prompt="", events=[], people=[]):
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

    def copy_with_changes(self, setting=None, prompt=None, events=None, people=None):
        return TranscriptState(
          setting=setting if setting else self.setting,
          prompt=prompt if prompt else self.prompt,
          events=events if events else self.events,
          people=people if people else self.people
        )

    def dict(self):
        overviews = list(map(lambda person: person.overview(), self.people)) 
        names = list(map(lambda person: person.name, self.people))
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
{", ".join(names)}

{"".join(overviews)}

Remember this information is only revealed by each person and only if the user asks the right questions.

            """,
            "events": self.events
        }

class Evidence:
  def __init__(self, presentation=""):
    self.presentation = f"{presentation}\n"
  
class ImageEvidence(Evidence):
  def __init__(self, url, description):
    self.description = description
    self.presentation = f"""
      ![]({url})
      _{description}_
    """

EVIDENCE = {
  "BUTCH_INTERVIEWED": ImageEvidence("https://i.redd.it/93a45ibm68tz.png", "Butch Atwood being interviewed by a local TV station"),
  "MAURA_MISSING_POSTER": ImageEvidence("https://allthatsinteresting.com/wordpress/wp-content/uploads/2018/05/maura-murray-missing-poster.png", "Missing Poster for Maura Murray"),
  "MAURA_AT_ATM": ImageEvidence("https://allthatsinteresting.com/wordpress/wp-content/uploads/2018/05/maura-murray-last-sighting.jpg", "February 9, 2004: Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store")
}

cartridge = {
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
  setting = """
Haverhill, New Hampshire. Morning at the scene of a black 1996 Saturn sedan up against the snowbank along Route 112, also known as Wild Ammonoosuc Road. 
The car is pointed west on the eastbound side of the road. The windshield is cracked and the car appears to have been involved in a collision
  """,
  prompt = """
  """,
  events=[],
  people=[PEOPLE["BUTCH_ATWOOD"], PEOPLE["FAITH_WESTMAN"], PEOPLE["CECIL_SMITH"], PEOPLE["JOHN_MONAGHAN"], PEOPLE["JEFF_WILLIAMS"]]
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
)

UMASS_START_DEFINITION = UMASS_DEFINITION.set_events(
  []
).dict()

CRIME_SCENE_START_DEFINITION = CRIME_SCENE_DEFINITION.set_events(
  []
).dict()

INTRO_TO_EVIDENCE_LOCKER_DEFINITION = TranscriptState(
  setting="A carefully guarded room in the FBI New Hampshire office with lockers containing evidence for different cases",
  prompt="""
There is one evidence locker Mike shows the user that is for the Maura Murray case. He will explain to the user that
evidence is still coming in but it will be divided into three boxes.
- Box 1: Photos
- Box 2: Official records
- Box 3: Other documents like timelines, maps, and notes

Only box one has anything in it, and it's photos of the scene of the accident. 
  """,
  events=[
    { "target": "INTRO_TO_EVIDENCE_LOCKER_ELB1", "if_the_user": "asks to open Box 1."},
    { "target": ".SELF", "if_the_user": "asks to open Box 2."},
    { "target": ".SELF", "if_the_user": "asks to open Box 3."},
  ],
  people=[]
).dict()

class EvidenceLocker(CherryPicker):
    def __init__(self, previous_state, go_back_if_the_user="asks to go back", prompt="", evidence_boxes=[], events_to_pick=[]):
      self.evidence_boxes = evidence_boxes
      super().__init__("EVIDENCE_LOCKER", previous_state, go_back_if_the_user, prompt, events_to_pick)

class EvidenceBox:
  def __init__(self, number, evidence=[]):
    self.number = number
    self.name = f"Box #{number}"
    self.evidence = evidence

  def add_evidence(self, evidence):
    self.evidence.append(evidence)

BOX_1_INITIAL_STATE = EvidenceBox(1, [
  EVIDENCE["MAURA_AT_ATM"], 
  EVIDENCE["MAURA_MISSING_POSTER"], 
  EVIDENCE["BUTCH_INTERVIEWED"]
])

elb1_options = ""
for evidence in BOX_1_INITIAL_STATE.evidence:
      elb1_options = f"{elb1_options}- {evidence.description}\n"

elb1_presentations = ""
for evidence in BOX_1_INITIAL_STATE.evidence:
      elb1_presentations = f"{elb1_presentations}## {evidence.description}\n\n{evidence.presentation}\n\n"

ELB1_INTRO_TO_EVIDENCE_LOCKER = BackForwardState(
  name="ELB1",
  previous_state="INTRO_TO_EVIDENCE_LOCKER",
  prompt=f"""
    The user can view the following evidence. List out all the
    options by name. If they request one, show the full presentation.

    # Options
    { elb1_options }

    # Presentations
    { elb1_presentations }
  """
)
ELB1_INTRO_TO_EVIDENCE_LOCKER.add_events([
  { 
    "target": Map("INTRO_TO_EVIDENCE_LOCKER", "map_map2_fbi_data_lab").state_name(), 
    "if_the_user": "asks_to_see_the_map" 
  }
])

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
  people = [PEOPLE["FRED_MURRAY"]]
).dict()

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
  ]
).dict()

POLICE_PRECINCT_DEFINITION = TranscriptState(
  setting = "The office of an anonyous investigator at a police precinct near the University of Massachusettes at Amherst",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["ANONYMOUS_INVESTIGATOR"]]
)

WORK_FRIEND_DEFINITION = TranscriptState(
  setting = "Back at the Murray household where now Fred and an anonymous work friend of Maura's are seated in the living room.",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["ANONYMOUS_WORK_FRIEND"], PEOPLE["FRED_MURRAY_2"], PEOPLE["BILLY"]]
).dict()

JULIE_MURRAY_DEFINITION = TranscriptState(
  setting = "A local coffee shop in Hanson Massachusettes where Julie Murray is seated with a coffee.",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["JULIE_MURRAY"]]
).dict()

MAURA_APARTMENT_DEFINITION = TranscriptState(
  setting = "Maura's apartment with her landlord. A Haverhill police officer is also there with items found in Maura's car",
  prompt = """
    Maura's things are all in boxes. It is unclear if she packed those boxes before leaving or if she just never unpacked them
    before moving in.
    There were also reports of a letter left in the dorm room addressed to Billy.
  """,
  events = [],
  people = [PEOPLE["ANONYMOUS_HAVERHILL_OFFICER"], PEOPLE["BILLY"]]
)

RED_TRUCK_WITNESS_DEFINITION = TranscriptState(
  setting = "Haverhill Swiftwater General Store where a witness waits outside to talk with Mike and the user",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["RED_TRUCK_WITNESS"]]
)

FRED_MURRAY_WITH_KNIFE_DEFINITION = TranscriptState(
  setting = "December 8, 2004. The Murray family house. Fred, Julie, and Kathleen Murray are all seated in the living room",
  prompt = """
  """,
  events = [],
  people = [PEOPLE["FRED_MURRAY_3"], PEOPLE["JULIE_MURRAY"], PEOPLE["KATHLEEN_MURRAY"]]
).dict()

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
  **cartridge,

  # Choices to go to either UMass or the crime scene
  "UMASS_1": UMASS_1_DEFINITION,
  "CRIME_SCENE_1": CRIME_SCENE_1_DEFINITION,

  # Same choices in an alternate order
  "CRIME_SCENE_2": CRIME_SCENE_2_DEFINITION,
  "UMASS_2": UMASS_2_DEFINITION,

  # Introduced to the map where they can revisit those two places.
  "INTRO_TO_MAP": INTRO_TO_MAP_DEFINITION,

  # Continued narrative backbone to now look at emails and searches
  # Just before the disappearance
  "DATA_LAB": DATA_LAB_DEFINITION.dict(),
    **Map("DATA_LAB", "map_map2_fbi_data_lab").key_dict(),

  # Crime scene and UMass again, but now in the model narrative backbones
  # will resemble going forwards where they have backforward states
  # Evidence locker hasn't been introduced yet.
  "CRIME_SCENE_START": CRIME_SCENE_START_DEFINITION,
    **Map("CRIME_SCENE_START", "map_map2_fbi_data_lab").key_dict(),

  "UMASS_START": UMASS_START_DEFINITION,
    **Map("UMASS_START", "map_map2_fbi_data_lab").key_dict(),

  # Continuing the backbone from the data lab, the next state is an introduction
  # to the evidence locker where they can review evidence they've gathered
  # Similar to the dummy non-reversible intro to map, this will also be a dummy
  # but those going forwards won't be.
  "INTRO_TO_EVIDENCE_LOCKER": INTRO_TO_EVIDENCE_LOCKER_DEFINITION,
    **ELB1_INTRO_TO_EVIDENCE_LOCKER.key_dict(),
    **Map(previous_state="INTRO_TO_EVIDENCE_LOCKER", map_key="map_map2_fbi_data_lab", events_to_pick=[]).key_dict(),

  # From this state, they can go to the next part of the narrative backbone
  # which is to advance the day to February 10th and visit Fred. 
  "VISIT_FRED": VISIT_FRED_DEFINITION,

  # Then, dawn the next day where a ground and air search begins. A dog search leads
  # Maura's scent 100 yards east until it stops. Here we also reveal the unaccounted hour of driving time.
  "SEARCH_FOR_MAURA": SEARCH_FOR_MAURA_DEFINITION,

  # Then, a talk with a police officer who was involved in an arrest of Maura two
  # a few months earlier for Credit Card fraud.
  "POLICE_PRECINCT": POLICE_PRECINCT_DEFINITION.dict(),

  # Then, we'll talk to a work friend of hers visiting Fred's place who can both tell the story both of her going
  # car shopping, then borrowing dad's car, then going to the party and having to
  # get back in an inexplicable hurry. This can also cover the call from the sister since it happened
  # at work and this is a work friend.
  "WORK_FRIEND": WORK_FRIEND_DEFINITION,

  # Then, we go to Julie's place where we can cover the boyfriend Billy.
  # This can also bring up the strange voicemail Billy got
  "JULIE_MURRAY": JULIE_MURRAY_DEFINITION,

  # Then, we go to Maura's apartment where there is the directions to Burlington VT and a book about
  # Hiking accidents
  "MAURA_APARTMENT": MAURA_APARTMENT_DEFINITION.dict(),

  # Then, the witness who saw the red truck at the general store.
  "RED_TRUCK_WITNESS": RED_TRUCK_WITNESS_DEFINITION.dict(),

  # Then, we go back to Fred's where he has received the rusted stained knife.
  "FRED_MURRAY_WITH_KNIFE": FRED_MURRAY_WITH_KNIFE_DEFINITION,

  # Then, the A-frame. The final state where they can actually move freely to all nodes.
  "A_FRAME_FINAL": TranscriptState(
    setting = "October 4, 2006. An A-Frame house approximately 1 mile from the crash site, nestled in the woods.",
    prompt = """
    """,
    events = FINAL_MAP_EL_EVENTS,
    people = [PEOPLE["TRUTH_SEEKER"]]
  ).dict(),

  # TODO: BackForward states get jumbled. May need to do this one by hand.
    **Map(
      previous_state = "EVIDENCE_LOCKER",
      map_key = "map_final"
    ).hard_set_events(FINAL_STATE_EVENTS + [
      {
        "target": "EVIDENCE_LOCKER_MAP",
        "if_the_user": "Wants to go to the evidence locker"
      }
    ]).key_dict(),
    **EvidenceLocker(
      previous_state="MAP"
    ).hard_set_events([
      {
        "target": "MAP_EVIDENCE_LOCKER",
        "if_the_user": "Wants to go to the map"
      }
    ]).key_dict(),

  # The rest of these nodes are copies (where needed) to permanently put the individuals in places
  # where the user can move to and interview. So the map is basically the central node for now.
  "U_MASS_FINAL": UMASS_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS).dict(),
  "CRIME_SCENE_FINAL": CRIME_SCENE_DEFINITION.copy_with_changes(events = FINAL_MAP_EL_EVENTS,
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