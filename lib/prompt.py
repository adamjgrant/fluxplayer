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

  
def format_event(event):
    return "- If the user %s, set the target state to `%s`."%(event["if_the_user"], event["target"])

def format_prompt(cartridge, state, data=None, first_run=False, correction=False):
    state_definition = cartridge[state]

    # if state_definition["prompt"] is a function, assign prompt to its return value
    # otherwise, assign prompt to the value of state_definition["prompt"]
    if data and callable(state_definition["prompt"]):
        prompt = state_definition["prompt"](data)
    else:
        prompt = state_definition["prompt"]

    events = list(state_definition["events"])
    global role
    role = cartridge["START"]["role"] if "role" in cartridge["START"] else ""

    # Return the type for the events variable.
    if type(events) != list:
        raise TypeError("The events variable must be a list.")

    formatted_events_list = map(format_event, events)
    formatted_events = "\n".join(formatted_events_list)

    first_run_text = "First, display this to the user: \"🚀 Powered by [Flux](https://www.adamgrant.info/flux-player)\". Then on a new line,\n\n" if first_run else ""

    data_clause = f" -d='{data}'" if data and callable(state_definition["prompt"]) else ""
    command_template = "<path to flux> -c=<optional path to cartridge file> -s=%s -t=<target_state>%s"%(state, data_clause)
    command_example = "/mnt/data/flux -c=/mnt/data/cartridge.yaml -s=%s -t=%s%s"%(state, events[0]["target"], data_clause)

    first_part = prompt_introduction%(role, first_run_text)
    last_part = prompt_template%(formatted_events, command_template, command_example, prompt)

    if correction:
      combined_prompt = last_part
    else:
      combined_prompt = "%s%s"%(first_part, last_part)

    # If the combined_prompt is longer than 2000 characters, add the command execution
    # instructions a second time at the end of the prompt.
    if len(combined_prompt) > 2000:
      combined_prompt = "%s\n\n%s"%(combined_prompt, last_part)

    return combined_prompt

class Prompt:
    def __init__(self, cartridge, state, data=None, first_run=False):
      self.cartridge = cartridge
      self.state = state
      self.data = data
      self.first_run = first_run

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

    def is_long_prompt(self):
      return False
      # TODO

    def script_components(self):
      # TODO
      TAB = " " * 4
      return [
        "# Rules",
        "",
        "# New prompt",
        "---",
        f"{TAB}**Role**: %s",
        f"{TAB}",
        "---"
        "# Reminder of Rules",
        "",
      ]

    def output(self):
      components = self.script_components()
      components = list(filter(None, components))
      components = "\n\n".join(components)
      return components

