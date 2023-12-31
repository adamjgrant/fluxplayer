#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Python script that takes a python file as input and imports the cartridge variable.

import argparse
from lib.path_reader import find_cartridge, convert_and_save_python_to_yaml
from lib.prompt import format_prompt

def cli():
  return Flux().parse_for_path()

class Flux:
  def parse_for_path(self):
      parser = argparse.ArgumentParser(description="Flux player")
      parser.add_argument("-c", "--cartridge", help="Relative or absolute path to the cartridge file")
      parser.add_argument("-s", "--state", help="State transitioning from")
      parser.add_argument("-t", "--transition", help="State to transition to")
      parser.add_argument("-d", "--data", help="Data to pass to the prompt function")
      parser.add_argument("-x", "--export", help="Export a Python cartridge to a YAML file", action="store_true")
      args = parser.parse_args()
      flux = Flux()
      return flux.main(args.cartridge, args.state, args.transition, args.data, args.export)

  def call_method_on_state(self, cartridge, state, target_state, data=None, first_run=False):
      if target_state == ".SELF":
          target_state = state

      if state not in cartridge:
          raise ValueError("The state %s does not exist in the cartridge. Try creating the command again."%state)

      state_definition = cartridge[state]

      # Find the object in the events list that has the method name.
      event = next((event for event in state_definition["events"] if event["target"] == target_state), None)

      # Throw an error if the event is not found
      if event == None and target_state != state:
          helpful_message = format_prompt(cartridge, state, data, first_run)
          advisory = "Please let the user know this was not a valid transition."
          raise ValueError("The state %s is not a valid transition from the state %s.\n\n%s\n\n%s"%(target_state, state, advisory, helpful_message))

      # Get the state definition for the target state.
      target_state_definition = cartridge[target_state]

      # Throw an error if the target state is not found
      if target_state_definition == None:
          raise ValueError("The target state %s does not exist in the cartridge."%target_state)

      return format_prompt(cartridge, target_state, data, first_run=first_run)

  def start_cartridge(self, cartridge):
      return format_prompt(cartridge=cartridge, state="START", first_run=True)

  # Output the cartridge variable as JSON.
  def main(self, path=None, state=None, transition=None, data=None, export=False):
      # Export cartridge
      if export:
          return convert_and_save_python_to_yaml(path)

      # Run cartridge
      try:
          cartridge = find_cartridge(path)
          current_state = state if state else "START"
          transition = transition if transition else None

          if (current_state == "START" and transition == None): 
            return print(self.start_cartridge(cartridge))

          else:
            return print(self.call_method_on_state(cartridge, current_state, transition, data))
      
      except FileNotFoundError as e:
          print(e)  # Print the error message if the file is not found

if __name__ == "__main__":
    flux = Flux()
    flux.parse_for_path()