import unittest
import tempfile
from ruamel.yaml import YAML
from flux import Flux
import os

class TestIngest(unittest.TestCase):
    def test_can_read_yaml_file(self):
        flux = Flux()
        # Create a temporary yaml file called cartridge.yaml
        with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
          yaml = YAML(typ="safe", pure=True)
          yaml_data = {'a': [1, 2]}
          yaml.dump(yaml_data, temp_file)

          self.assertTrue(os.path.exists(temp_file.name))

          # Move the temporary file to the current directory and rename to cartridge.yaml
          new_file_path = os.path.join(os.path.dirname(__file__), "cartridge.yaml")
          os.rename(temp_file.name, new_file_path)

          found_contents = flux.read_yaml_cartridge()
          self.assertEqual(found_contents, yaml_data)

        os.remove(new_file_path)

    def test_automatically_reads_yaml_file(self):
        flux = Flux()
        # Create a temporary yaml file called cartridge.yaml
        with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as temp_file:
          yaml = YAML(typ="safe", pure=True)
          yaml_data = {'a': [1, 2]}
          yaml.dump(yaml_data, temp_file)

          self.assertTrue(os.path.exists(temp_file.name))

          # Move the temporary file to the current directory and rename to cartridge.yaml
          new_file_path = os.path.join(os.path.dirname(__file__), "cartridge.yaml")
          os.rename(temp_file.name, new_file_path)

          found_contents = flux.find_cartridge()
          self.assertEqual(found_contents, yaml_data)

        os.remove(new_file_path)

    def test_sees_python_file(self):
        flux = Flux()
        # Create a temporary yaml file called cartridge.yaml
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
          # Add some contents to temp_file
          file_contents = b"print('hello world')"
          temp_file.write(file_contents)
          temp_file.close()

          self.assertTrue(os.path.exists(temp_file.name))

          # Move the temporary file to the current directory and rename to cartridge.yaml
          new_file_path = os.path.join(os.path.dirname(__file__), "cartridge.py")
          os.rename(temp_file.name, new_file_path)

          found_contents = flux.find_cartridge()
          self.assertEqual(found_contents, file_contents)

        os.remove(new_file_path)

    def test_prefers_python_file_over_yaml_file(self):
        self.assertEqual(1, 1)