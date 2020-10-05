#!/bin/sh

mypy --ignore-missing-imports .
black .
isort --profile black .
