#!/bin/bash
set -eo pipefail

COLOR_GREEN=$(tput setaf 2)
COLOR_NC=$(tput sgr0) # No Color

echo "Starting black"
poetry run black .
echo "OK"

echo "Starting isort"
poetry run isort .
echo "OK"

echo "Starting ruff"
poetry run ruff check --select I --fix
poetry run ruff check --fix
echo "OK"

echo "${COLOR_GREEN}✨ Code formatted and linted successfully!${COLOR_NC}"
