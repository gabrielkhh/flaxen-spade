#!/bin/sh

python -m mypy --ignore-missing-imports --pretty .
python -m black .
python -m isort --profile black .
