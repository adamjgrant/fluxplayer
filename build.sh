#!/bin/zsh

RELEASE="2.0.3"

rm -rf dist
mkdir -p dist
mkdir -p dist/openai
mkdir -p dist/linux

echo "Generating cartridges..."
python3 flux.py -c examples/find_maura_murray/cartridge.py -x

echo "Building project for Linux/OpenAI..."
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
cp -r dist/linux/flux dist/openai/flux

echo "Publishing GitHub release..."
gh release create v$RELEASE ./dist/

echo "Build completed."

echo "Building for pip distribution..."
python3 -m build -o dist/pip/*
echo "Publishing pip distribution..."
python3 -m twine upload --repository testpypi dist/pip/*

# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps flux-player-adamjgrant