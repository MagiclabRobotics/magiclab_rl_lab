#!/bin/bash

# switch to script directory
cd "$(dirname "$0")"

# choose python interpreter
PYTHON="/home/ubuntu/miniconda3/envs/mmckit/bin/python"

# script path
TRAIN_SCRIPT="scripts/rsl_rl/train.py"

# run
$PYTHON $TRAIN_SCRIPT \
    --task=Magiclab-Z1-12dof-Velocity \
    --run_name=z1_12dof_test \
    --headless \
    --max_iterations=10000 \
    --num_envs=8192 \
    --device=cuda:0 \
    # --resume \
    # --load_run=2025-12-03_15-49-25_mlz1_12_dof_policy_v3_bs_v2_change_correct_order \
    # --checkpoint=model_1600.pt