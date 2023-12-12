# Python script that takes a python file as input and imports the cartridge variable.

import sys
import importlib.util
import os
from ruamel import yaml

class Flux:
  role = None

  def import_cartridge(path):
        # Check if the file exists
      if not os.path.exists(path):
          raise FileNotFoundError(f"The file {path} does not exist.")

      spec = importlib.util.spec_from_file_location("cartridge", path)
      cartridge = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(cartridge)
      return cartridge.cartridge

  def format_event(event):
      return "- If the user %s, send the `%s` event."%(event["if_the_user"], event["method"])

  def format_prompt(state_definition, state, first_run=False):
      prompt = state_definition["prompt"]
      events = state_definition["events"]
      global role

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

  def call_method_on_state(cartridge, state, method, first_run=False):
      if state not in cartridge:
          raise ValueError("The state %s does not exist in the cartridge."%state)

      state_definition = cartridge[state]

      # Find the object in the events list that has the method name.
      event = next((event for event in state_definition["events"] if event["method"] == method), None)

      # Throw an error if the event is not found
      if event == None:
          raise ValueError("The event %s does not exist in the state %s."%(method, state))

      # Get the state definition for the target state.
      target_state = event["target"]
      target_state_definition = cartridge[target_state]

      # Throw an error if the target state is not found
      if target_state_definition == None:
          raise ValueError("The target state %s does not exist in the cartridge."%target_state)

      return format_prompt(target_state_definition, target_state, first_run=first_run)

  def start_cartridge(cartridge):
      return format_prompt(cartridge["START"], "START", True)

  # Output the cartridge variable as JSON.
  def main():
      if len(sys.argv) < 2:
          print("Usage: python3 flux.py <path_to_cartridge.yaml> [current_state] [transition]")
          return

      try:
          with open(sys.argv[1], 'r') as file:
            cartridge = yaml.safe_load(file)
          current_state = sys.argv[2] if len(sys.argv) > 2 else "START"
          transition = sys.argv[3] if len(sys.argv) > 3 else None
          global role
          role = cartridge["START"]["role"] if "role" in cartridge["START"] else ""

          if (current_state == "START" and transition == None): 
            return print(start_cartridge(cartridge))

          else:
            return print(call_method_on_state(cartridge, current_state, transition))

          print(start_cartridge(cartridge))
      except FileNotFoundError as e:
          print(e)  # Print the error message if the file is not found

  if __name__ == "__main__":
      main()