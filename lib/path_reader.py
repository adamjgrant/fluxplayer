#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Python script that takes a python file as input and imports the cartridge variable.

import sys
import importlib
import os
from ruamel.yaml import YAML
from pathlib import Path
import argparse

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    exe_path = os.path.dirname(sys.executable)
    print("exe_path: %s"%exe_path)
    root_dir = Path(exe_path).resolve().parent
    print("root_dir: %s"%root_dir)
else:
    root_dir = Path(__file__).resolve().parent.parent

def get_absolute_path(relative_path):
    # Check if the path is already absolute
    if os.path.isabs(relative_path):
        return relative_path

    # Get the directory of the current script
    global root_dir

    # Join the script directory with the relative path
    return os.path.join(root_dir, relative_path)

def read_yaml_cartridge(path=None):
    yaml = YAML()

    # Load cartridge.yaml at the same directory as this file.
    with open(path, 'r') as file:
        cartridge = yaml.load(file)

    return cartridge

def read_python_cartridge(path=None):
    # Load cartridge.py at the same directory as this file.
    sys.path.append(os.path.dirname(path))
    module_name = os.path.basename(path).replace(".py", "")
    module = importlib.import_module(module_name)
    cartridge = getattr(module, "cartridge")
    return cartridge

def detect_full_catridge_path(path=None):
    # If path is None, check if a cartridge.yaml or cartridge.py exists in the same directory as this file.
    global root_dir
    if path is None:
      # Check for a cartridge.yaml or cartridge.py in the same directory as this file.
      yaml_path = os.path.join(root_dir, "cartridge.yaml")
      found_yaml = os.path.exists(yaml_path)
      python_path = os.path.join(root_dir, "cartridge.py")
      found_python = os.path.exists(python_path)
      if not found_yaml and not found_python:
        raise FileNotFoundError("Could not find a .yaml or .py at %s."%root_dir)
      path = yaml_path if found_yaml else python_path

    # Regardless of this file existing, let's normalize to an absolute path.
    full_path = get_absolute_path(path)

    # If path doesn't have an extension, check for a .py file first, then a .yaml file.
    ext = Path(full_path).suffix
    if not ext:
      if os.path.exists(full_path + ".yaml"):
        full_path = full_path + ".yaml"
      elif os.path.exists(full_path + ".py"):
        full_path = full_path + ".py"
      else:
        raise FileNotFoundError("Could not find a .yaml or .py at %s."%root_dir)

    return full_path

def find_cartridge(path=None):
    cartridge = None
    full_path = detect_full_catridge_path(path)
    is_python = Path(full_path).suffix == ".py"

    if is_python:
      cartridge = read_python_cartridge(full_path)
    else:
      cartridge = read_yaml_cartridge(full_path)
    
    return cartridge