from __future__ import annotations

import torch
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv
    from isaaclab.managers import SceneEntityCfg
    from isaaclab.sensors import ContactSensor

'''
def gait_phase(env: ManagerBasedRLEnv, period: float) -> torch.Tensor:
    if not hasattr(env, "episode_length_buf"):
        env.episode_length_buf = torch.zeros(env.num_envs, device=env.device, dtype=torch.long)

    global_phase = (env.episode_length_buf * env.step_dt) % period / period

    phase = torch.zeros(env.num_envs, 2, device=env.device)
    phase[:, 0] = torch.sin(global_phase * torch.pi * 2.0)
    phase[:, 1] = torch.cos(global_phase * torch.pi * 2.0)

    cmd_norm = torch.norm(env.command_manager.get_command("base_velocity"), dim=1)

    # for i, val in enumerate(cmd_norm):
    #     if val < 0.01:
    #         print("环境", i, "cmd_norm =", val.item())

    phase[:, 0][cmd_norm < 0.02] = 0
    phase[:, 1][cmd_norm < 0.02] = 1

    return phase

'''
def gait_phase(env: ManagerBasedRLEnv, period: float) -> torch.Tensor:
    if not hasattr(env, "episode_length_buf"):
        env.episode_length_buf = torch.zeros(env.num_envs, device=env.device, dtype=torch.long)

    global_phase = (env.episode_length_buf * env.step_dt) % period / period
    
    # return float mask 1 is stance, 0 is swing
    phase = global_phase
    sin_pos = torch.sin(2 * torch.pi * phase)
    # Add double support phase
    stance_mask = torch.zeros((env.num_envs, 2), device=env.device)
    # left foot stance
    stance_mask[:, 0] = sin_pos >= 0
    # right foot stance
    stance_mask[:, 1] = sin_pos < 0

    cmd_norm = torch.norm(env.command_manager.get_command("base_velocity"), dim=1)

    stance_mask[:, 0][cmd_norm < 0.02] = 1
    stance_mask[:, 1][cmd_norm < 0.02] = 1

    return stance_mask


def contact_mask(
    env: ManagerBasedRLEnv,
    sensor_cfg: SceneEntityCfg,             
) -> torch.Tensor:
    contact_sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    contact_mask = (contact_sensor.data.net_forces_w[:, sensor_cfg.body_ids, 2]) > 5

    return contact_mask
