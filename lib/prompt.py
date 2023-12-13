role = None
  
def format_event(event):
    return "- If the user %s, send the `%s` event."%(event["if_the_user"], event["method"])

def format_prompt(cartridge, state, first_run=False):
    state_definition = cartridge[state]
    prompt = state_definition["prompt"]
    events = list(state_definition["events"])
    global role
    role = cartridge["START"]["role"] if "role" in cartridge["START"] else ""

    # Return the type for the events variable.
    if type(events) != list:
        raise TypeError("The events variable must be a list.")

    formatted_events_list = map(format_event, events)
    formatted_events = "\n".join(formatted_events_list)

    first_run_text = "First, display this to the user: \"🚀 Powered by [Flux](https://www.adamgrant.info/flux-player)\". Then on a new line, " if first_run else ""

    return """
%s

Your new prompt is:

--- 

%s%s

---

# Responding to the user

Listen to how the user responds and choose the best event from the list below.
Only use one listed. Do not make up a new one:

%s

# Running the command

Run the command similarly to how you did before and include the state and event they chose in the following format:

`<path to flux.py> <path to cartridge.yaml> %s <event>`

For example

`/mnt/data/flux.py /mnt/data/cartridge.yaml %s %s` 
    """%(role, first_run_text, prompt, formatted_events, state, state, events[0]["method"])