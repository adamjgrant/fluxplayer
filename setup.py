# setup.py
import os
from setuptools import setup

import my_package

dev_version = os.environ.get("VERSION")

setup(
  version=dev_version if dev_version else f"{my_package.__version__}"
)