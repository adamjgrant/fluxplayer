# Python script that takes a python file as input and imports the cartridge variable.

import sys
import importlib.util
import json
import os

def import_cartridge(path):
      # Check if the file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

    spec = importlib.util.spec_from_file_location("cartridge", path)
    cartridge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cartridge)
    return cartridge.cartridge

# Output the cartridge variable as JSON.
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 flux.py <path_to_cartridge.py>")
        return

    try:
        cartridge = import_cartridge(sys.argv[1])
        print(cartridge)
    except FileNotFoundError as e:
        print(e)  # Print the error message if the file is not found

if __name__ == "__main__":
    main()