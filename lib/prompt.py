#!/usr/local/bin/python
# -*- coding: utf-8 -*-
role = None
prompt_template = """%s
Your new prompt is:

---

%s%s

---

# Responding to the user

No matter what the user says, **do not respond**. You **must first run a command** to get your new prompt based on the user's response.

Choose the best fitting event from the list below.
Only use one listed. Do not make up a new one:

%s

# Running the command

Run the command similarly to how you did before and include the state and event they chose in the following format:

`%s`

For example

`%s`
"""

  
def format_event(event):
    return "- If the user %s, send the `%s` event."%(event["if_the_user"], event["method"])

def format_prompt(cartridge, state, data=None, first_run=False):
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
    command_template = "<path to flux> -c=<optional path to cartridge file> -s=%s -t=<event>%s"%(state, data_clause)
    command_example = "/mnt/data/flux -c=/mnt/data/cartridge.yaml -s=%s -t=%s%s"%(state, events[0]["method"], data_clause)

    return prompt_template%(role, first_run_text, prompt, formatted_events, command_template, command_example)