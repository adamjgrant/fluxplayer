from examples.find_maura_murray.lib.special_states import CherryPicker
from examples.find_maura_murray.lib.image import Image
from examples.find_maura_murray.lib.event_self import EVENT_SELF

# Evidence Sets just have multiple pieces of evidence. Just a way of organizing a bunch of related things.
# However, we can also give the user options to go deep on one piece of evidence like reading a full transcript.
# For this, there are Evidence Trails. These appear as a piece of evidence but allow drilling down into a few
# different paths by only one level.


class Evidence:
  def __init__(self, date, time=None, presentation="", description=""):
    self.presentation = f"{presentation}\n"
    self.description = description
    self.date = date
    self.time = time
  
class ImageEvidence(Evidence):
  def __init__(self, url, description, date, time=None):
    presentation = Image(url=url, description=description).markdown()
    super().__init__(description=description, presentation=presentation, date=date, time=time)

class EvidenceSet:
  def __init__(self, evidences=[], description=""):
    self.evidences = evidences
    self.description = description
    self.presentation = ""

    for evidence in evidences:
      self.presentation += evidence.presentation

class EvidenceTrail(Evidence):
  def __init__(
    self, 
    date, 
    time=None, 
    presentation="", 
    description="", 
    evidence_set_objects=[], 
    key="",
    previous_backbone_state="EVIDENCE_LOCKER",
    previous_backbone_state_description="Evidence Locker"
  ):
    super().__init__(date, time, presentation, description)
    self.key = key
    # Evidence set objects are EvidenceSet instances as values of the keys of the states they represent
    # like { "EVIDENCE_SET_A": EvidenceSet(evidences=[evidence_1, evidence_2], description="description_a")}
    self.evidence_set_objects = evidence_set_objects
    self.previous_backbone_state = previous_backbone_state
    self.previous_backbone_state_description = previous_backbone_state_description

  def key_dict(self):
    _key_dict = {}
    _key_dict[self.key] = {
      "prompt": """
Let the user know they are now in an area of the evidence locker where they can see the evidence described in the events below.
The user will need to choose either to see an evidence set or to go back to a previous state. 
      """,
      "events": [
        { "target": "EVIDENCE_LOCKER", "if_the_user": "wants to go back or back specifically to the evidence locker" },
        { "target": self.previous_backbone_state, "if_the_user": f"wants to go back to {self.previous_backbone_state_description}" }
      ]
    }
    for evidence_set_object in self.evidence_set_objects:
      key = next(iter(evidence_set_object))
      evidence_set = evidence_set_object[key]
      _key_dict[self.key]["events"].append({ "target": f"{self.key}_{key}", "if_the_user": f"wants to see evidence that includes: {evidence_set.description}" }) 

    for evidence_set_object in self.evidence_set_objects:
      evidence_set = evidence_set_object[next(iter(evidence_set_object))]
      _key_dict[f"{self.key}_{next(iter(evidence_set_object))}"] = {
        "prompt": f"""
Let the user know they are now looking at a small set of evidence in the evidence locker for "{evidence_set.description}" 
and the evidence is as follows:

{evidence_set.presentation}
        """,
        "events": [
          { "target": "EVIDENCE_LOCKER", "if_the_user": "wants to go back or back specifically to the evidence locker" },
          { "target": self.key, "if_the_user": "wants to go back to the evidence set where they were before but not all the way back to the evidence locker" },
          { "target": self.previous_backbone_state, "if_the_user": f"wants to go back to {self.previous_backbone_state_description}" }
        ]
      }
    return _key_dict

EVIDENCE = {
  "BUTCH_ATWOOD": EvidenceSet(evidences = [
    ImageEvidence(url="butch_atwood_interview.png", description="Butch Atwood being interviewed by a local TV station", date="February 10, 2024"),
    ImageEvidence(url="butch_atwood_home.png", description="Butch Atwood being interviewed by a local TV station", date="February 10, 2024")
  ], description="Images of Butch Atwood around his home near the time of Maura Murray's disappearance"),
  "MAURA_MISSING_POSTER": ImageEvidence(url="missingposter.gif", description="Missing Poster for Maura Murray", date="2024"),
  "MAURA_AT_ATM": EvidenceSet(evidences = [
    ImageEvidence(url="maura_atm_01.png", description="Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store", date="February 9, 2024"),
    ImageEvidence(url="maura_atm_02.png", description="Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store", date="February 9, 2024"),
    ImageEvidence(url="maura_atm_03.png", description="Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store", date="February 9, 2024"),
    ImageEvidence(url="maura_atm_04.png", description="Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store", date="February 9, 2024"),
    ImageEvidence(url="maura_atm_05.png", description="Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store", date="February 9, 2024")
  ], description="Security camera footage of Maura Murray at ATM"),
  "MAURAS_COMPUTER": Evidence(date="February 9, 2024", description="Computer records collected in the data lab from Maura Murray's computer", presentation="""
Data gathered about Maura Murray's activities on February 9, the day she disappeared:
Email to Boyfriend: At 1:00 PM, Maura emailed her boyfriend, expressing affection and promising to call later.
Phone Call Inquiries: She made a call inquiring about a rental property in Bartlett, New Hampshire.
Email to Professor: Maura sent an email to her professor at UMass, indicating she would be out of town for a week due to a death in the family.
MapQuest Searches: She used her computer to search for directions to the Berkshires and Burlington, Vermont.
Hotel Inquiry: At 2:05 PM, she called a number for hotel bookings in Stowe, Vermont, lasting about five minutes.
Voicemail to Boyfriend: At 2:18 PM, Maura left a voicemail for her boyfriend, saying they would talk later.
ATM Withdrawal: At 3:15 PM, security footage shows Maura withdrawing $280 from an ATM, nearly all the money in her account. She was alone.
Liquor Store Visit: Shortly after, footage shows her purchasing $40 worth of alcohol, including Baileys, Kahlúa, vodka, and Franzia wine, at a liquor store. She was alone.
Final Phone Usage: The last recorded use of her cell phone was at 4:37 PM, when she checked her voicemail.
  """)
}

# TODO: Evidence locker should pick these up, assign the right previous states before adding them
# to the evidence locker.
# TODO: It should also make individual events on the evidence locker state to get to evidence trails.
EVIDENCE_TRAILS = {
  "TRANSCRIPTS": EvidenceTrail(
    key="TRANSCRIPTS",
    date="Various",
    description="Transcripts of interviews with people involved in the case",
    evidence_set_objects=[
      {
        "Faith Westman 911 call": EvidenceSet(evidences=[
          Evidence(
            date="February 9, 2024",
            description="911 call with Faith Westman",
            presentation="""
Recording from Grafton County Dispatch Case F-04-1514

G1: Grafton County Dispatcher Marsh, can I help you?

FW: Yes, um, we apparently have a car that has gone off the road here outside our home.

G1: Ok, is anybody hurt?

FW: Um, I have not gone out to investigate, um...

G1: Ok.

G1: Are you in Bath, correct?

FW: Uh, well actually, um, no, Haverhill. I'm on the Weathered Barn, um.

G1: Oh, you're at the Weathered Barn, ok.

D1: Grafton, this is 911. I show it as [Inaudible].

G1: Mhmm, right [Inaudible]. Yup, that is Haverhill. Ok, um, very good. Is this Faith I'm speaking with?

FW: Yes.

G1: And is your phone number [Redacted]?

FW: Correct.

G1: And your address is [Redacted]?

FW: Right.

G1: Ok, I'll be sending an Officer.

FW: Ok, [inaudible] around the corner from the barn.

G1: So after the barn?

FW: Yeah.

G1: Ok.

G1: Ok, very good. I'm sending an Officer.

FW: Yeah.

G1: Ok?

FW: Ok, thanks [inaudible].

G1: Thanks, Faith [inaudible].

FW: Yeah, bye-bye.
            """
          )
        ])
      }
    ]
  )
}

class EvidenceLocker(CherryPicker):
    def __init__(
      self, 
      previous_state, 
      go_back_if_the_user="asks to go back", 
      prompt="", 
      events_to_pick=[], 
      evidence_object=EVIDENCE, 
      evidence_trails=EVIDENCE_TRAILS,
      level="", 
      next_backbone=""):
      super().__init__("EVIDENCE_LOCKER", previous_state, go_back_if_the_user, prompt, events_to_pick + [EVENT_SELF])
      self.evidence_object = evidence_object
      self.evidence_trails = evidence_trails
      self.level = level
      self.next_backbone = next_backbone
      self.prompt = f"""
Setting: A carefully guarded room in the FBI New Hampshire office with lockers containing evidence for different cases
Mike will give the user a list of evidence currently on file and will explain how additional evidence will be gathered
as they progress to visit more places and talk to more people. He will also explain that they can always ask to go back to
the map to visit another location to review evidence or talk to someone. All they have to do is ask.

Mike can give the user a list of evidence available:
{self.evidence_as_list()}

If the user asks to see some evidence, here is what Mike can show for each item:
{self.evidence_as_catalogue()}
      """
      
    # This exists so we can add the EvidenceTrail items and modify them based on context
    def generated_evidence_object(self):
      evidence_object = {
        **self.evidence_object,
        **self.evidence_trails
      }
      return evidence_object

    def add_evidence(self, key, value):
      self.evidence_object[key] = value 

    def evidence_as_list(self):
      x = 1
      list_as_str = ""
      evidence_object = self.generated_evidence_object()
      for key in evidence_object:
        description = evidence_object[key].description
        list_as_str += f"{x} - {description}\n"
        x = x + 1
      return list_as_str

    def evidence_as_catalogue(self):
      x = 1
      catalogue_as_str = ""
      evidence_object = self.generated_evidence_object()
      for key in evidence_object:
        description = evidence_object[key].description
        presentation = evidence_object[key].presentation
        catalogue_as_str += f"{x} - {description}\n{presentation}\n\n"
        x = x + 1
      return catalogue_as_str

    def state_name(self):
      return super().state_name() + (f"_{self.level}" if self.level else "")

