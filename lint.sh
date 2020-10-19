#!/bin/sh

python -m mypy --ignore-missing-imports .
python -m black .
python -m isort --profile black .
