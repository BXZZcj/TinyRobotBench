import mplib.planner
import sapien.core as sapien
from sapien.utils import Viewer
import mplib


def move_to_pose(    
        viewer: Viewer,
        robot: sapien.Articulation, 
        urdf_file_path: str,
        srdf_file_path: str,
        move_group: str,
        pose: sapien.Pose,
        time_step=1/100,
        joint_vel_limits=[],
        joint_acc_limits=[],
        n_render_step=4,
) -> int:
    
    def setup_planner() -> mplib.Planner:
        link_names = [link.get_name() for link in robot.get_links()]
        joint_names = [joint.get_name() for joint in robot.get_active_joints()]
        planner = mplib.Planner(
            urdf=urdf_file_path,
            srdf=srdf_file_path,
            user_link_names=link_names,
            user_joint_names=joint_names,
            move_group=move_group,
            joint_vel_limits=joint_vel_limits,
            joint_acc_limits=joint_acc_limits)
        return planner

    def follow_path(result: dict) -> None:
        scene=viewer.scene
        active_joints = robot.get_active_joints()
        n_step = result['position'].shape[0]
        n_driven_joints=result['position'].shape[1]

        for i in range(n_step):  
            # qf = robot.compute_passive_force(
            #     gravity=True, 
            #     coriolis_and_centrifugal=True)
            # robot.set_qf(qf)
            for j in range(n_driven_joints):
                active_joints[j].set_drive_target(result['position'][i][j])
                # print(result['position'][i][j])
                active_joints[j].set_drive_velocity_target(result['velocity'][i][j])
            scene.step()
            if i % n_render_step == 0:
                scene.update_render()
                viewer.render()
    

    planner=setup_planner()   
    pose_list = list(pose.p)+list(pose.q)
    # Screw Algo
    result = planner.plan_screw(pose_list, robot.get_qpos(), time_step=time_step)
    if result['status'] != "Success":
        # RTTConnect Algo
        result = planner.plan_qpos_to_pose(pose_list, robot.get_qpos(), time_step=time_step)
        if result['status'] != "Success":
            # print(result['status'])
            return -1 
    follow_path(result=result)
    return 0