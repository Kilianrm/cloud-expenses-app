#!/bin/bash
set -e

# Build the image first
docker-compose build

# Run the container interactively
docker-compose run --rm cdk

