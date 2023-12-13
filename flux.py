# Python script that takes a python file as input and imports the cartridge variable.

import sys
import importlib
import os
from ruamel.yaml import YAML
import pathlib
import argparse

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
  
  def parse_for_path(self):
      parser = argparse.ArgumentParser(description="Flux player")
      parser.add_argument("-c", "--cartridge", help="Relative or absolute path to the cartridge file")
      args = parser.parse_args()
      flux = Flux()
      return flux.main(args.cartridge)

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
      yaml = YAML()

      # Load cartridge.yaml at the same directory as this file.
      with open(path, 'r') as file:
          cartridge = yaml.load(file)

      return cartridge

  def read_python_cartridge(self, path=None):
      # Load cartridge.py at the same directory as this file.
      sys.path.append(os.path.dirname(path))
      module_name = os.path.basename(path).replace(".py", "")
      module = importlib.import_module(module_name)
      cartridge = getattr(module, "cartridge")
      return cartridge

  def detect_full_catridge_path(self, path=None):
      # If path is None, check if a cartridge.yaml or cartridge.py exists in the same directory as this file.
      if path is None:
        # Check for a cartridge.yaml or cartridge.py in the same directory as this file.
        yaml_path = os.path.join(os.path.dirname(__file__), "cartridge.yaml")
        found_yaml = os.path.exists(yaml_path)
        python_path = os.path.join(os.path.dirname(__file__), "cartridge.py")
        found_python = os.path.exists(python_path)
        if not found_yaml and not found_python:
          raise FileNotFoundError("Could not find a cartridge.yaml or cartridge.py at %s."%os.path.dirname(__file__))
        path = yaml_path if found_yaml else python_path

      # Regardless of this file existing, let's normalize to an absolute path.
      full_path = get_absolute_path(path)

      # If path doesn't have an extension, check for a .py file first, then a .yaml file.
      ext = pathlib.Path(full_path).suffix
      if not ext:
        if os.path.exists(full_path + ".yaml"):
          full_path = full_path + ".yaml"
        elif os.path.exists(full_path + ".py"):
          full_path = full_path + ".py"
        else:
          raise FileNotFoundError("Could not find a .yaml or .py at %s."%os.path.dirname(full_path))

      return full_path

  def find_cartridge(self, path=None):
      cartridge = None
      full_path = self.detect_full_catridge_path(path)
      is_python = pathlib.Path(full_path).suffix == ".py"

      if is_python:
        cartridge = self.read_python_cartridge(full_path)
      else:
        cartridge = self.read_yaml_cartridge(full_path)
      
      return cartridge

  # Output the cartridge variable as JSON.
  def main(self, path=None):
      yaml = YAML()
      if len(sys.argv) < 1:
          print("Usage: flux [-c=cartridge_to_use] [current_state] [transition]")
          return

      try:
          cartridge = self.find_cartridge(path)
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
    flux = Flux()
    flux.parse_for_path()