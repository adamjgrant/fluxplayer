#!/bin/zsh

RELEASE="2.0.4"

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
gh release create v$RELEASE ./dist/openai/flux --title "Flux Player v$RELEASE" --notes "To use this release in a custom GPT, download flux from the assets below" --prerelease

echo "Build completed."

echo "Building for pip distribution..."
poetry build
echo "Publishing pip distribution..."
python3 -m twine upload --repository testpypi dist/pip/*

# python3 -m pip3 install --index-url https://test.pypi.org/simple/ --no-deps flux-player-adamjgrant