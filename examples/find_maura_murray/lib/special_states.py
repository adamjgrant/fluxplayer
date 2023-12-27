from examples.find_maura_murray.lib.image import Image
from examples.find_maura_murray.lib.event_self import EVENT_SELF

class BackForwardState():
    def __init__(self, name="", previous_state="", go_back_if_the_user="asks to go back", prompt=""):
      self.events = [ { "target": previous_state, "if_the_user": go_back_if_the_user } ]
      self.prompt = prompt
      self.name = name
      self.previous_state = previous_state

    def add_events(self, events=[]):
      self.events = self.events + events
      return self

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
      super().__init__("MAP", previous_state, "asks to go back", prompt, events_to_pick + [EVENT_SELF])
      self.map_key = map_key
      image = Image(url=f"{map_key}.png", description="Map of key locations").markdown()
      self.prompt = f"""
{prompt}

Remember to show the user a map like this:
{image}
      """

class TranscriptState:
    def __init__(self, setting, prompt="", events=[], people=[], next_backbone=None):
        self.prompt = prompt
        self.events = events + [EVENT_SELF]
        self.people = people
        self.setting = setting
        self.next_backbone = next_backbone

    def set_events(self, events):
        self.events = events + [EVENT_SELF]
        return self

    def copy_with_changes(self, setting=None, prompt=None, events=None, people=None, next_backbone=None):
        # We do this because it always adds EVENT_SELF each time we make a new transcript state.
        if events:
          _events = events
        else:
          _events = self.events
          _events.pop()

        return TranscriptState(
          setting=setting if setting else self.setting,
          prompt=prompt if prompt else self.prompt,
          events=_events,
          people=people if people else self.people,
          next_backbone=next_backbone if next_backbone else self.next_backbone
        )

    def user_menu(self):
        if self.next_backbone:
          return f"""
Lastly, add this to your message at the bottom:
_🗺️ Map has a new item: "{self.next_backbone}". Ask for the map to go there or anywhere else_
          """
        else:
          return ""

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
{self.user_menu()}

            """,
            "events": self.events
        }