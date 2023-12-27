#!/bin/zsh

echo "Generating cartridges..."
python3 flux.py -c examples/find_maura_murray/cartridge.py -x

echo "Building project for Linux..."
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux

echo "Build completed."

echo "Building for pip distribution..."
python3 -m build -o dist/pip/
echo "Publishing pip distribution..."
python3 -m twine upload --repository testpypi dist/pip/*