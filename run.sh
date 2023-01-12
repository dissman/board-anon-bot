#!/bin/bash

source ./venv/bin/activate
while true; do
    python3 main.py
    if [ $? -ne 0 ]; then
        echo "An exception occurred. Restarting program..."
    else
        break
    fi
done
