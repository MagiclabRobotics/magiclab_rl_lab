# Magiclab RL Lab

[![IsaacSim](https://img.shields.io/badge/IsaacSim-5.1.0-silver.svg)](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html)
[![Isaac Lab](https://img.shields.io/badge/IsaacLab-2.3.0-silver)](https://isaac-sim.github.io/IsaacLab)


## Overview

This project provides a set of reinforcement learning environments for MagicLab robots, built on top of [IsaacLab](https://github.com/isaac-sim/IsaacLab).

Currently supports MagicLab **Z1-12dof** robots.

## Installation

- Install Isaac Lab by following the [installation guide](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html).
- Install the Magiclab RL IsaacLab standalone environments.

  - Clone or copy this repository separately from the Isaac Lab installation (i.e. outside the `IsaacLab` directory):

    ```bash
    git clone https://github.com/MagiclabRoboticsrobotics/magiclab_rl_lab.git
    ```
  - Use a python interpreter that has Isaac Lab installed, install the library in editable mode using:

    ```bash
    conda activate env_isaaclab
    ./magiclab_rl_lab.sh -i
    # restart your shell to activate the environment changes.
    ```

- Verify that the environments are correctly installed by:

  - Listing the available tasks:

    ```bash
    ./magiclab_rl_lab.sh -l # This is a faster version than isaaclab
    ```
  - Running a task:

    ```
    python scripts/rsl_rl/train.py --headless --task Magiclab-Z1-12dof-Velocity
    ```
    or
    ```
    ./train_bash.sh
    ```

  - Inference with a trained agent:

    ```bash
    python scripts/rsl_rl/play.py --task Magiclab-Z1-12dof-Velocity
    ```

    or

    ```
    ./play_bash.sh
    ```

    if you want to use keyboard control, use:

    ```
    ./play_keyboard_bash.sh
    ```

## Deploy

After the model training is completed, we need to perform sim2sim on the trained strategy in Mujoco to test the performance of the model.
Then deploy sim2real.

## Acknowledgements

This repository is built upon the support and contributions of the following open-source projects. Special thanks to:

- [IsaacLab](https://github.com/isaac-sim/IsaacLab): The foundation for training and running codes.
- [mujoco](https://github.com/google-deepmind/mujoco.git): Providing powerful simulation functionalities.
- [robot_lab](https://github.com/fan-ziqi/robot_lab): Referenced for project structure and parts of the implementation.
- [whole_body_tracking](https://github.com/HybridRobotics/whole_body_tracking): Versatile humanoid control framework for motion tracking.
