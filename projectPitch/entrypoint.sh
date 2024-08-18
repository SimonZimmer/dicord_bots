#!/bin/sh
set -xe

# Install dependencies
poetry install

# Run the Python script
poetry run python source/projectPitch.py
