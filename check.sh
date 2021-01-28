#!/bin/bash

mypy --strict `find . -not \( -path ./venv -prune \) -name "*.py"`
