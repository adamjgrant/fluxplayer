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
    def __init__(self, previous_state, go_back_if_the_user="asks to go back", prompt="", events_to_pick=[]):
      super().__init__("EVIDENCE_LOCKER", previous_state, go_back_if_the_user, prompt, events_to_pick)