import sapien.core as sapien
from sapien.utils import Viewer

from .core import *


class PandaGrasp:
    def __init__(
            self,
            viewer: Viewer,
            robot: sapien.Articulation, 
            urdf_file_path: str,
            srdf_file_path: str,
            gripper: str,
            pregrasp_target_distance=[0.0, 0, 0.3],
            grasp_target_distance=[0.0, 0, 0.09],
            time_step=1/100,
            joint_vel_limits=[],
            joint_acc_limits=[],
            n_render_step=4,
    ):
        self.viewer=viewer
        self.scene=self.viewer.scene
        self.robot=robot
        self.urdf_file_path=urdf_file_path
        self.srdf_file_path=srdf_file_path
        self.gripper=gripper
        self.pregrasp_target_distance=pregrasp_target_distance
        self.grasp_target_distance=grasp_target_distance
        self.time_step=time_step
        self.joint_vel_limits=joint_vel_limits
        self.joint_acc_limits=joint_acc_limits
        self.n_render_step=n_render_step

        self.gripper_grasp_rotation=[0,1,0,0]
    

    def _move_to_pose(
            self,
            pose: sapien.Pose
    ) -> int:
        return move_to_pose(    
            self.viewer,
            self.robot, 
            self.urdf_file_path,
            self.srdf_file_path,
            self.gripper,
            pose,
            self.time_step,
            self.joint_vel_limits,
            self.joint_acc_limits,
            self.n_render_step,
            )                    


    def move_for_grasp( 
            self,  
            target_pose: sapien.Pose,
    ) -> int:
        # The gripper is above the target, refered to as pregrasp
        target_pose_translation=list(target_pose.p)
        target_pose_translation=[a + b for a, b in zip(target_pose_translation, self.pregrasp_target_distance)]
        pregrasp_pose=sapien.Pose(target_pose_translation, self.gripper_grasp_rotation)
        self._move_to_pose(pregrasp_pose)


    def _open_gripper(
            self, 
            target=0.4
    ) -> None:
        for joint in self.robot.get_active_joints()[-2:]:
            joint.set_drive_target(target)
        for i in range(100): 
            qf = self.robot.compute_passive_force(
                gravity=True, 
                coriolis_and_centrifugal=True)
            self.robot.set_qf(qf)
            self.scene.step()
            if i % self.n_render_step == 0:
                self.scene.update_render()
                self.viewer.render()

    def _close_gripper(self) -> None:
        for joint in self.robot.get_active_joints()[-2:]:
            joint.set_drive_target(0)
        for i in range(100):  
            qf = self.robot.compute_passive_force(
                gravity=True, 
                coriolis_and_centrifugal=True)
            self.robot.set_qf(qf)
            self.scene.step()
            if i % self.n_render_step == 0:
                self.scene.update_render()
                self.viewer.render()


    def grasp(self) -> None:
        self._open_gripper()

        for link in self.robot.get_links():
            if link.get_name()==self.gripper:
                pregrasp_pose=link.get_pose()
                pregrasp_translation=list(pregrasp_pose.p)
                break
        grasp_translation=pregrasp_translation
        grasp_translation=[a-b for a,b in zip(grasp_translation,self.pregrasp_target_distance)]
        grasp_translation=[a+b for a,b in zip(grasp_translation,self.grasp_target_distance)]
        grasp_pose=sapien.Pose(grasp_translation, self.gripper_grasp_rotation)

        self._move_to_pose(grasp_pose)

        self._close_gripper()

        self._move_to_pose(pregrasp_pose)

    
    def ungrasp(self) -> None:
        self._open_gripper()