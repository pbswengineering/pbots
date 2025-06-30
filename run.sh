#!/usr/bin/env bash

VENV="$HOME/.virtualenvs/pbots/bin/python"
if [ -f "$VENV" ]; then
    echo "Using virtualenv"
    PYTHON="$VENV"
else
    echo "Using default interpreter"
    PYTHON='python3'
fi
cd -P -- "$(dirname -- "$0")"
"$PYTHON" main.py "$@"
