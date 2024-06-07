#!/bin/bash

# Activate Conda Environment
source activate fbx-env

# Run Python script for Command 3
python fbx_utils/merge_an.py

# Deactivate Conda Environment
conda deactivate
