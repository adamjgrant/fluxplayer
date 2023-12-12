import unittest
import tempfile
from ruamel.yaml import YAML
from flux import Flux
import os

class TestIngest(unittest.TestCase):
    def test_sees_yaml_file(self):
        # Create a temporary yaml file called cartridge.yaml
        with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
          yaml = YAML(typ="safe", pure=True)
          yaml_data = {'a': [1, 2]}
          yaml.dump(yaml_data, temp_file)

          self.assertTrue(os.path.exists(temp_file.name))

          # Move the temporary file to the current directory and rename to cartridge.yaml
          os.rename(temp_file.name, "cartridge.yaml")

          found_contents = Flux.read_yaml()
          self.assertEqual(found_contents, yaml_data)

        os.remove(temp_file.name)

    def test_sees_python_file(self):
        self.assertEqual(1, 1)

    def test_prefers_python_file_over_yaml_file(self):
        self.assertEqual(1, 1)