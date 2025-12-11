# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import isaaclab.sim as sim_utils
from isaaclab.actuators import IdealPDActuatorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.utils import configclass

MAGICLAB_MODEL_DIR = "path/to/magiclab_model"  # Replace with the actual path to your magiclab_model directory
MAGICLAB_ROS_DIR = "/home/ubuntu/xbh/ws/magiclab_lab_clean"  # Replace with the actual path to your magiclab_ros package


@configclass
class MagiclabArticulationCfg(ArticulationCfg):
    """Configuration for Magiclab articulations."""

    joint_sdk_names: list[str] = None

    soft_joint_pos_limit_factor = 0.9


@configclass
class MagiclabUsdFileCfg(sim_utils.UsdFileCfg):
    activate_contact_sensors: bool = True
    rigid_props = sim_utils.RigidBodyPropertiesCfg(
        disable_gravity=False,
        retain_accelerations=False,
        linear_damping=0.0,
        angular_damping=0.0,
        max_linear_velocity=1000.0,
        max_angular_velocity=1000.0,
        max_depenetration_velocity=1.0,
    )
    articulation_props = sim_utils.ArticulationRootPropertiesCfg(
        enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=4
    )


@configclass
class MagiclabUrdfFileCfg(sim_utils.UrdfFileCfg):
    fix_base: bool = False
    activate_contact_sensors: bool = True
    replace_cylinders_with_capsules = True
    joint_drive = sim_utils.UrdfConverterCfg.JointDriveCfg(
        gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0, damping=0)
    )
    articulation_props = sim_utils.ArticulationRootPropertiesCfg(
        enabled_self_collisions=True,
        solver_position_iteration_count=8,
        solver_velocity_iteration_count=4,
    )
    rigid_props = sim_utils.RigidBodyPropertiesCfg(
        disable_gravity=False,
        retain_accelerations=False,
        linear_damping=0.0,
        angular_damping=0.0,
        max_linear_velocity=1000.0,
        max_angular_velocity=1000.0,
        max_depenetration_velocity=1.0,
    )

    def replace_asset(self, meshes_dir, urdf_path):
        """Replace the asset with a temporary copy to avoid modifying the original asset.

        When need to change the collisions, place the modified URDF file separately in this repository,
        and let `meshes_dir` be provided by `magiclab_ros`.
        This function will auto construct a complete `robot_description` file structure in the `/tmp` directory.
        Note: The mesh references inside the URDF should be in the same directory level as the URDF itself.
        """
        tmp_meshes_dir = "/tmp/IsaacLab/magiclab_rl_lab/meshes"
        if os.path.exists(tmp_meshes_dir):
            os.remove(tmp_meshes_dir)
        os.makedirs("/tmp/IsaacLab/magiclab_rl_lab", exist_ok=True)
        os.symlink(meshes_dir, tmp_meshes_dir)

        self.asset_path = "/tmp/IsaacLab/magiclab_rl_lab/robot.urdf"
        if os.path.exists(self.asset_path):
            os.remove(self.asset_path)
        os.symlink(urdf_path, self.asset_path)


""" Configuration for the Magiclab robots."""

MAGICLAB_Z1_12DOF_CFG = MagiclabArticulationCfg(
    spawn=MagiclabUrdfFileCfg(
        asset_path=f"{MAGICLAB_ROS_DIR}/source/magiclab_rl_lab/magiclab_rl_lab/data/robots/magicbot-Z1/urdf/MagicBotZ1_arm_ready_pos.urdf",
    ),
    # spawn=MagiclabUsdFileCfg(
    #     usd_path=f"{MAGICLAB_MODEL_DIR}/G1/23dof/usd/g1_23dof_rev_1_0/g1_23dof_rev_1_0.usd",
    # ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.69),
        joint_pos={
            "JOINT_HIP_ROLL_.*": 0.0,
            "JOINT_HIP_YAW_.*": 0.0,
            "JOINT_HIP_PITCH_.*": -0.35,
            "JOINT_KNEE_PITCH_.*": 0.7,
            "JOINT_ANKLE_PITCH_.*": -0.35, #NOTE: v11_use_old_ready_pos
            "JOINT_ANKLE_ROLL_.*": 0.0,
            # "joint_.*a1": 0.0,
        },
        joint_vel={".*": 0.0},
    ),
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=[
                "JOINT_HIP_ROLL_.*",
                "JOINT_HIP_YAW_.*",
                "JOINT_HIP_PITCH_.*",
                "JOINT_KNEE_PITCH_.*",
            ],
            effort_limit_sim=120,
            velocity_limit_sim=20,
            stiffness={
                "JOINT_HIP_PITCH_.*": 100.0,
                "JOINT_HIP_ROLL_.*": 100.0,
                "JOINT_HIP_YAW_.*": 100.0,
                "JOINT_KNEE_PITCH_.*": 150.0,
            },
            damping={
                "JOINT_HIP_PITCH_.*": 4.0,
                "JOINT_HIP_ROLL_.*": 4.0,
                "JOINT_HIP_YAW_.*": 4.0,
                "JOINT_KNEE_PITCH_.*": 5.0,
            },
            armature={
                "JOINT_HIP_.*": 0.02863,
                "JOINT_KNEE_.*": 0.02863,
            },
        ),
        "feet": ImplicitActuatorCfg(
            effort_limit_sim=50,
            velocity_limit_sim=15,
            joint_names_expr=["JOINT_ANKLE_PITCH_.*", "JOINT_ANKLE_ROLL_.*"],
            stiffness=60.0,
            damping=3.0,
            armature=0.01503,
        ),
    },
    joint_sdk_names=[
        "JOINT_HIP_PITCH_L",
        "JOINT_HIP_ROLL_L",
        "JOINT_HIP_YAW_L",
        "JOINT_KNEE_PITCH_L",
        "JOINT_ANKLE_PITCH_L",
        "JOINT_ANKLE_ROLL_L",

        "JOINT_HIP_PITCH_R",
        "JOINT_HIP_ROLL_R",
        "JOINT_HIP_YAW_R",
        "JOINT_KNEE_PITCH_R",
        "JOINT_ANKLE_PITCH_R",
        "JOINT_ANKLE_ROLL_R",
    ],
)