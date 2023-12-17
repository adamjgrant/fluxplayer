#!/usr/local/bin/python
# -*- coding: utf-8 -*-
role = None
prompt_introduction = """%s
# Responding to the user

No matter what the user says, **do not respond**. You **must first run a command** to get your new prompt based on the user's response.
%s
"""
prompt_template = """Choose the best fitting event from the list below.
Only use one listed. Do not make up a new one:

%s

# Running the command

Run the command similarly to how you did before and include the state and event they chose in the following format:

`%s`

For example

`%s`

# Your new prompt is

%s

"""

class Prompt:
    def __init__(self, cartridge, state, data=None, first_run=False, connection=False):
      self.cartridge = cartridge
      self.state = state
      self.data = data
      self.first_run = first_run
      self.connection = connection
      self.state_definition = cartridge[state]
      self.role = cartridge["START"]["role"] if "role" in cartridge["START"] else ""
      self._events = list(self.state_definition["events"])
      
      # Return the type for the events variable.
      if type(self._events) != list:
          raise TypeError("The events variable must be a list.")

      # if state_definition["prompt"] is a function, assign prompt to its return value
      # otherwise, assign prompt to the value of state_definition["prompt"]
      if data and callable(self.state_definition["prompt"]):
          self.inner_prompt = self.state_definition["prompt"](data)
      else:
          self.inner_prompt = self.state_definition["prompt"]

      # Prompt Anatomy
      #
      #
      # # Rules
      # [1. Warning that the machine should not respond but run a command with command examples.]
      # 
      # # New prompt
      #
      # ---
      #
      # **Role**: [2. Optional role]
      # [3. The new prompt it should follow starting with showing the flux intro if this is the first run]
      #
      # ---
      #
      # [# Reminder of Rules (Show this heading again if the prompt is very long)]
      #
      # [4. Second Warning that the machine should not respond but run a command with command examples if the prompt is very long.]

    def events(self):
      formatted_events_list = map(format_event, self._events)
      formatted_events = "\n".join(formatted_events_list)
      return formatted_events

    def rules(self):
      data_clause = f" -d='{self.data}'" if self.data and callable(self.state_definition["prompt"]) else ""
      command_template = "<path to flux> -c=<optional path to cartridge file> -s=%s -t=<target_state>%s"%(self.state, data_clause)
      command_example = "/mnt/data/flux -c=/mnt/data/cartridge.yaml -s=%s -t=%s%s"%(self.state, self._events[0]["target"], data_clause)
      return f"""
Run the command similarly to how you did before and include the state and event they chose in the following format:

`{command_template}`

For example

`{command_example}`
      """

    def is_long_prompt(self):
      return len(self.inner_prompt) > 2000

    def script_components(self):
      return [
        "No matter what the user says, **do not respond**. You **must first run a command** to get your new prompt based on the user's response.",
        "# Rules",
        self.rules(),
        "# New prompt",
        "---",
        f"**Role**: {self.role}" if self.role else "",
        f"{self.inner_prompt}",
        "---",
        "# Reminder of Rules" if self.is_long_prompt() else "",
        self.rules() if self.is_long_prompt() else "",
      ]

    def output(self):
      components = self.script_components()
      components = list(filter(None, components))
      components = "\n\n".join(components)
      return components

  
def format_event(event):
    return "- If the user %s, set the target state to `%s`."%(event["if_the_user"], event["target"])

def format_prompt(cartridge, state, data=None, first_run=False, correction=False):
    return Prompt(cartridge, state, data, first_run, correction).output()