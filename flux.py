# Python script that takes a python file as input and imports the cartridge variable.

import sys
import importlib.util
import os

def import_cartridge(path):
      # Check if the file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

    spec = importlib.util.spec_from_file_location("cartridge", path)
    cartridge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cartridge)
    return cartridge.cartridge

def format_event(event):
    return "\nIf the user %s, send the `%s` event."%(event["user_behavior"], event["method"])

def format_prompt(state_definition):
    prompt = state_definition["prompt"]
    events = state_definition["events"]

    # Return the type for the events variable.
    if type(events) != list:
        raise TypeError("The events variable must be a list.")

    formatted_events_list = map(format_event, events)
    formatted_events = "".join(formatted_events_list)

    return "%s\n%s"%(prompt, formatted_events)

def call_method_on_state(cartridge, state, method):
    if state not in cartridge:
        raise ValueError("The state %s does not exist in the cartridge."%state)

    state_definition = cartridge[state]

    if method not in state_definition:
        raise ValueError("The method %s does not exist in the state %s."%(method, state))

    return format_prompt(state_definition[method])

def start_cartridge(cartridge):
    return format_prompt(cartridge["START"])

# Output the cartridge variable as JSON.
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 flux.py <path_to_cartridge.py> [current_state] [transition]")
        return

    try:
        cartridge = import_cartridge(sys.argv[1])
        current_state = sys.argv[2] if len(sys.argv) > 2 else "START"
        transition = sys.argv[3] if len(sys.argv) > 3 else None

        if (current_state == "START" and transition == None): 
          return print(start_cartridge(cartridge))

        else:
          return print(call_method_on_state(cartridge, current_state, transition))

        print(start_cartridge(cartridge))
    except FileNotFoundError as e:
        print(e)  # Print the error message if the file is not found

if __name__ == "__main__":
    main()