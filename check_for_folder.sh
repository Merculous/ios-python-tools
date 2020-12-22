#!/bin/bash

path="venv/lib/python3.8/site-packages/iospytools"

if [ -e $path ]; then
    echo "$path exists!"
else
    echo "$path does not exist!"
fi
