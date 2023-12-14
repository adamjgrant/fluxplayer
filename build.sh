#!/bin/bash

echo "Building project for Linux..."
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux

echo "Build completed."