#!/bin/bash

if [ -e ./venv ]; then
    # load virtual environment, if one exists
    echo "Found virtual environment, source it" >&2
    source ./venv/bin/activate
    # assume it was created by this script
elif ! python3 checklxml.py; then
    # create a new virtual environment
    echo "lxml module does not exists, create virtual environment" >&2
    python -m venv ./venv
    source ./venv/bin/activate
    echo "install lxml" >&2
    pip install -q --cache-dir ./.pip ./external/lxml-4.3.4-cp36-cp36m-manylinux1_x86_64.whl >&2
fi

python3 ./main.py $@
