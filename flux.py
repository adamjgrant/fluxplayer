#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Python script that takes a python file as input and imports the cartridge variable.

import sys
import os
import argparse
from lib.path_reader import find_cartridge
from lib.prompt import format_prompt

class Flux:
  def parse_for_path(self):
      parser = argparse.ArgumentParser(description="Flux player")
      parser.add_argument("-c", "--cartridge", help="Relative or absolute path to the cartridge file")
      parser.add_argument("-s", "--state", help="State in which to fire a transition")
      parser.add_argument("-t", "--transition", help="Transition to fire on state")
      parser.add_argument("-d", "--data", help="Data to pass to the prompt function")
      args = parser.parse_args()
      flux = Flux()
      cartridge = find_cartridge(args.cartridge)
      return flux.main(args.cartridge, args.state, args.transition, args.data)

  def call_method_on_state(self, cartridge, state, method, data=None, first_run=False):
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

      return format_prompt(cartridge, target_state, data, first_run=first_run)

  def start_cartridge(self, cartridge):
      return format_prompt(cartridge, "START", True)

  # Output the cartridge variable as JSON.
  def main(self, path=None, state=None, transition=None, data=None):
      if path is None and state is None and transition is None:
          print("Usage: flux [-c=cartridge_to_use] [-s=current_state] [-t=transition]")
          return

      try:
          cartridge = find_cartridge(path)
          current_state = state if state else "START"
          transition = transition if transition else None

          if (current_state == "START" and transition == None): 
            return print(self.start_cartridge(cartridge))

          else:
            # TODO I think we lost first run
            return print(self.call_method_on_state(cartridge, current_state, transition, data))
      
      except FileNotFoundError as e:
          print(e)  # Print the error message if the file is not found

if __name__ == "__main__":
    flux = Flux()
    flux.parse_for_path()