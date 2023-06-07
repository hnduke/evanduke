#!/bin/bash

echo "Checking for optional tag. If absent, the tag will default to \"latest\""
TAG=${1:-latest}

echo "Pulling updated app image..."
docker pull hnduke/evanduke:$TAG

echo "Taking old containers down..."
docker compose down

echo "Spinning up new containers..."
docker compose up -d

echo "Removing old images..."
# remove unused images
docker image prune -fa

echo "Deployed."
