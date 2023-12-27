from examples.find_maura_murray.lib.special_states import CherryPicker
from examples.find_maura_murray.lib.image import Image

class Evidence:
  def __init__(self, presentation="", description=""):
    self.presentation = f"{presentation}\n"
  
class ImageEvidence(Evidence):
  def __init__(self, url, description):
    self.presentation = Image(url=url, description=description).markdown()

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
      super().__init__("EVIDENCE_LOCKER", previous_state, go_back_if_the_user, prompt, events_to_pick)
      self.evidence_object = evidence_object
      self.level = level
      self.next_backbone = next_backbone
      self.prompt = f"""
Setting: A carefully guarded room in the FBI New Hampshire office with lockers containing evidence for different cases
Mike will give the user a list of evidence currently on file and will explain how additional evidence will be gathered
as they progress to visit more places and talk to more people. He will also explain that they can always ask to go back to
the map to visit another location to review evidence or talk to someone. All they have to do is ask.
{self.user_menu()}
      """

    def user_menu(self):
        if self.next_backbone:
          return f"""
Lastly, add this to your message at the bottom:
_🗺️ Map has a new item: "{self.next_backbone}". Ask for the map to go there or anywhere else_
          """
        else:
          return ""

    def state_name(self):
      return super().state_name() + (f"_{self.level}" if self.level else "")