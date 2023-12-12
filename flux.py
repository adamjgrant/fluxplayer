# Python script that takes a python file as input and imports the cartridge variable.

import sys
import importlib
import os
from ruamel.yaml import YAML
import pathlib

def get_absolute_path(relative_path):
    # Check if the path is already absolute
    if os.path.isabs(relative_path):
        return relative_path

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Join the script directory with the relative path
    return os.path.join(script_dir, relative_path)

class Flux:
  role = None

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

  def read_yaml_cartridge(self, path=None):
      path = get_absolute_path(path) if path else os.path.join(os.path.dirname(__file__), "cartridge.yaml") 
      yaml = YAML()

      # Load cartridge.yaml at the same directory as this file.
      with open(path, 'r') as file:
          cartridge = yaml.load(file)

      return cartridge

  def read_python_cartridge(self, path=None):
      # Load cartridge.py at the same directory as this file.
      path = get_absolute_path(path) if path else os.path.join(os.path.dirname(__file__), "cartridge.py")
      if not os.path.exists(path):
        return None
      else: 
        sys.path.append(os.path.dirname(path))
        module_name = os.path.basename(path).replace(".py", "")
        module = importlib.import_module(module_name)
        cartridge = getattr(module, "cartridge")
        return cartridge

  def find_cartridge(self, path=None):
      cartridge = None
      full_path = get_absolute_path(path) if path else os.path.join(os.path.dirname(__file__), "cartridge.py") 
      # If path has no extension, make it .py
      ext = pathlib.Path(full_path).suffix
      full_path = full_path + ".py" if not ext else full_path

      # Determine if the value of path is a python file.
      path_is_python = full_path.endswith(".py")
      python_cartridge = self.read_python_cartridge(full_path)

      if not python_cartridge or not path_is_python:
        full_path = path if path else os.path.join(os.path.dirname(__file__), "cartridge.yaml") 
        yaml_cartridge = self.read_yaml_cartridge(full_path)
        cartridge = yaml_cartridge
      else:
        cartridge = python_cartridge
      return cartridge

  # Output the cartridge variable as JSON.
  def main(self):
      yaml = YAML()
      if len(sys.argv) < 1:
          print("Usage: python3 flux.py [current_state] [transition]")
          return

      try:
          cartridge = self.find_cartridge()
          current_state = sys.argv[1] if len(sys.argv) > 1 else "START"
          transition = sys.argv[2] if len(sys.argv) > 2 else None
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