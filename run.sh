#!/usr/bin/env bash

ANACONDA="$HOME/anaconda3/bin/python"
if [ -f "$ANACONDA" ]; then
    PYTHON="$ANACONDA"
else
    PYTHON='python3'
fi
cd -P -- "$(dirname -- "$0")"
"$PYTHON" main.py "$@"
