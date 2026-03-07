#!/usr/bin/sh

set -euo pipefail

cd pico-sdk
conan create . --version $1
cd ..

cd picotool
conan create . --version $1
cd ..

cd pioasm
conan create . --version $1
cd ..

