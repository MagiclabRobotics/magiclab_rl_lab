#!/bin/bash

# switch to script directory
cd "$(dirname "$0")"

# choose python interpreter
PYTHON="/home/ubuntu/miniconda3/envs/mmckit/bin/python"

# script path
TRAIN_SCRIPT="scripts/rsl_rl/play_keyboard.py"

# run
$PYTHON $TRAIN_SCRIPT \
    --task=Magiclab-Z1-12dof-Velocity \
    --checkpoint=logs/rsl_rl/magiclab_z1_12dof_velocity/2025-12-11_09-45-00_z1_12dof_test/model_0.pt \
    --device=cuda:0 \
    --keyboard

