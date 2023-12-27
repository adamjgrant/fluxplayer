from examples.find_maura_murray.lib.special_states import CherryPicker
from examples.find_maura_murray.lib.image import Image
from examples.find_maura_murray.lib.event_self import EVENT_SELF

class Evidence:
  def __init__(self, presentation="", description=""):
    self.presentation = f"{presentation}\n"
  
class ImageEvidence(Evidence):
  def __init__(self, url, description):
    presentation = Image(url=url, description=description).markdown()
    super().__init__(description=description, presentation=presentation)
    self.description = description

class EvidenceSet:
  def __init__(self, evidences=[], description=""):
    self.evidences = evidences
    self.description = description
    self.presentation = ""

    for evidence in evidences:
      self.presentation += evidence.presentation

EVIDENCE = {
  "BUTCH_INTERVIEWED": ImageEvidence("butch_atwood_interview.png", "Butch Atwood being interviewed by a local TV station"),
  "BUTCH_ATWOOD_HOME": ImageEvidence("butch_atwood_home.png", "Butch Atwood being interviewed by a local TV station"),
  "MAURA_MISSING_POSTER": ImageEvidence("missingposter.gif", "Missing Poster for Maura Murray"),
  "MAURA_AT_ATM": EvidenceSet(evidences = [
    ImageEvidence("maura_atm_01.png", "February 9, 2004: Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store"),
    ImageEvidence("maura_atm_02.png", "February 9, 2004: Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store"),
    ImageEvidence("maura_atm_03.png", "February 9, 2004: Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store"),
    ImageEvidence("maura_atm_04.png", "February 9, 2004: Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store"),
    ImageEvidence("maura_atm_05.png", "February 9, 2004: Maura Murray at ATM seemingly alone withdrawing $280 before visiting liquor store")
  ], description="Security camera footage of Maura Murray at ATM")
}

class EvidenceLocker(CherryPicker):
    def __init__(self, previous_state, go_back_if_the_user="asks to go back", prompt="", events_to_pick=[], evidence_object=EVIDENCE, level="", next_backbone=""):
      super().__init__("EVIDENCE_LOCKER", previous_state, go_back_if_the_user, prompt, events_to_pick + [EVENT_SELF])
      self.evidence_object = evidence_object
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

    def evidence_as_list(self):
      x = 1
      list_as_str = ""
      for key in self.evidence_object:
        description = self.evidence_object[key].description
        list_as_str += f"{x} - {description}\n"
        x = x + 1
      return list_as_str

    def evidence_as_catalogue(self):
      x = 1
      catalogue_as_str = ""
      for key in self.evidence_object:
        description = self.evidence_object[key].description
        presentation = self.evidence_object[key].presentation
        catalogue_as_str += f"{x} - {description}\n{presentation}\n\n"
        x = x + 1
      return catalogue_as_str

    def state_name(self):
      return super().state_name() + (f"_{self.level}" if self.level else "")