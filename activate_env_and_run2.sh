#!/bin/bash

# Activate Conda Environment
source activate fbx-env

# Run Python script for Command 2
python fbx_utils/obj2fbx.py

# Deactivate Conda Environment
conda deactivate
