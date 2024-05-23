#!/bin/bash

# get the absolute path of current directory
CURRENT_DIR=$(pwd)

# add the current directory to PYTHONPATH
echo "export PYTHONPATH=\"\$PYTHONPATH:$CURRENT_DIR\"" >> ~/.bashrc

# reload .bashrc to immediately apply the change
source ~/.bashrc

echo "Added $CURRENT_DIR to PYTHONPATH."

# make sure your conda environment has been activated
echo "Note: make sure your conda environment has been activated."

# install dependencies with pip
pip install -r requirements.txt