#!/bin/zsh

source .env

echo "Publishing GitHub release..."
gh release create v$VERSION ./dist/openai/flux --title "Flux Player v$VERSION" --notes "To use this release in a custom GPT, download flux from the assets below" --prerelease

rm -rf dist
mkdir -p dist
mkdir -p dist/openai
mkdir -p dist/linux

# Create "Printed" cartridge.yaml
echo "Generating cartridges..."
poetry run flux -c examples/find_maura_murray/cartridge.py -x

echo "Building project for Linux/OpenAI..."
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux
cp -r dist/linux/flux dist/openai/flux

echo "Build completed."

echo "Building for pip distribution..."
poetry build
echo "Publishing pip distribution..."
python3 -m twine upload --repository testpypi dist/*.tar.gz

# python3 -m pip3 install --index-url https://test.pypi.org/simple/ --no-deps flux-player-adamjgrant