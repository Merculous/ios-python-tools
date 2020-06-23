#!/bin/bash

python setup.py bdist_wheel sdist

pip install -e .

