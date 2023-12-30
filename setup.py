# setup.py
import os
from setuptools import setup

dev_version = os.environ.get("VERSION")

setup(version=dev_version)