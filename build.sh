#!/bin/zsh

echo "Generating cartridges..."
python3 flux.py -c examples/find_maura_murray/cartridge.py -x

echo "Building project for Linux..."
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux

echo "Build completed."