import sapien.core as sapien
import mplib
import numpy as np
from sapien.utils.viewer import Viewer


def load_robot(
        scene: sapien.Scene,
        pose: sapien.Pose,
        init_qpos: list,
        urdf_file_path: str,
        fix_root_link=True,
        uniform_stiffness=1000,
        uniform_damping=200,
        name='',
) -> sapien.Articulation:
    # Robot
    # Load URDF
    loader: sapien.URDFLoader = scene.create_urdf_loader()
    loader.fix_root_link = fix_root_link
    robot: sapien.Articulation = loader.load(urdf_file_path)
    robot.set_root_pose(pose)
    robot.set_name(name=name)

    # Set initial joint positions
    robot.set_qpos(init_qpos)

    # Used for PID control
    active_joints = robot.get_active_joints()
    for joint_idx, joint in enumerate(active_joints):
        joint.set_drive_property(stiffness=uniform_stiffness, damping=uniform_damping)

    return robot
