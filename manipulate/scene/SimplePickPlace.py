import sapien.core as sapien
from sapien.utils import Viewer
import numpy as np
from transforms3d.euler import euler2quat

from utils import *
from api import *
from config import *

class SimplePickPlaceScene():
    def __init__(self):
        self.engine = sapien.Engine()
        self.renderer = sapien.SapienRenderer()
        self.engine.set_renderer(self.renderer)

        scene_config = sapien.SceneConfig()
        self.scene = self.engine.create_scene(scene_config)
        self.timestep = 1 / 100.0
        self.scene.set_timestep(self.timestep)
        self.scene.add_ground(-1)
        physical_material = self.scene.create_physical_material(static_friction=1, dynamic_friction=1, restitution=0.0)
        self.scene.default_physical_material = physical_material
        

        self.scene.set_ambient_light(color=[0.5, 0.5, 0.5])
        self.scene.add_directional_light(direction=[0, 1, -1], color=[0.5, 0.5, 0.5], shadow=True)
        self.scene.add_point_light(position=[1, 2, 2], color=[1, 1, 1], shadow=True)
        self.scene.add_point_light(position=[1, -2, 2], color=[1, 1, 1], shadow=True)
        self.scene.add_point_light(position=[-1, 0, 1], color=[1, 1, 1], shadow=True)

        self.viewer = Viewer(self.renderer)
        self.viewer.set_scene(self.scene)
        self.viewer.set_camera_xyz(x=1.46, y=0, z=0.6)
        self.viewer.set_camera_rpy(r=0, p=-0.8, y=np.pi)
        self.viewer.window.set_camera_parameters(near=0.05, far=100, fovy=1)

        self._create_tabletop()
        self._create_robot()

        self.grasp_tool=PandaGrasp(
            viewer=self.viewer,
            robot=self.robot, 
            urdf_file_path=self.robot_urdf_path,
            srdf_file_path=self.robot_srdf_path,
            gripper=self.move_group,
            joint_vel_limits=np.ones(7),
            joint_acc_limits=np.ones(7),
            time_step=self.timestep,
            )
    

    def _create_tabletop(self) -> None:
        # table top
        self.table=create_table(
            scene=self.scene,
            pose=sapien.Pose([0.56, 0, 0]),
            size=1.0,
            height=1,
            thickness=0.1,
            name="table",
            )

        # pads
        self.red_pad=create_box(
            scene=self.scene,
            pose=sapien.Pose([-0.3+0.56, 0.35, 0.005]),
            half_size=[0.1, 0.1, 0.005],
            color=[1., 0., 0.],
            name='red_pad',
        )
        self.green_pad=create_box(
            scene=self.scene,
            pose=sapien.Pose([0.56, 0.35, 0.005]),
            half_size=[0.1, 0.1, 0.005],
            color=[0., 1., 0.],
            name='green_pad',
        )
        self.blue_pad=create_box(
            scene=self.scene,
            pose=sapien.Pose([0.3+0.56, 0.35, 0.005]),
            half_size=[0.1, 0.1, 0.005],
            color=[0., 0., 1.],
            name='blue_pad',
        )

        #objects
        self.box = create_box(
            self.scene,
            sapien.Pose(p=[0.56, 0, 0.02], q=euler2quat(0, 0, np.pi/2)),
            half_size=[0.02, 0.05, 0.02],
            color=[1., 0., 0.],
            name='box',
        )
        self.sphere = create_sphere(
            self.scene,
            sapien.Pose(p=[-0.3+0.56, -0.4, 0.02]),
            radius=0.02,
            color=[0., 1., 0.],
            name='sphere',
        )
        self.capsule = create_capsule(
            self.scene,
            sapien.Pose(p=[0.3+0.3, 0.2, 0.02]),
            radius=0.02,
            half_length=0.03,
            color=[0., 0., 1.],
            name='capsule',
        )
        self.banana = load_object_mesh(
            self.scene, 
            sapien.Pose(p=[-0.2+0.56, 0, 0.01865]), 
            collision_file_path=manipulate_root_path+'assets/object/banana/collision_meshes/collision.obj',
            visual_file_path=manipulate_root_path+'assets/object/banana/visual_meshes/visual.dae',
            name='banana',
        )

    def _create_robot(self) -> None:
        self.robot_urdf_path=manipulate_root_path+"assets/robot/panda/panda.urdf"
        self.robot_srdf_path=manipulate_root_path+"assets/robot/panda/panda.srdf"
        self.move_group="panda_hand"
        # Robot
        # Load URDF
        self.init_qpos=[0, 0.19634954084936207, 0.0, -2.617993877991494, 0.0, 2.941592653589793, 0.7853981633974483, 0, 0]
        self.robot=load_robot(
            scene=self.scene,
            pose=sapien.Pose([0, 0, 0], [1, 0, 0, 0]),
            init_qpos=self.init_qpos,
            urdf_file_path=self.robot_urdf_path,
            name="panda_robot",
            )       

        self.active_joints = self.robot.get_active_joints()
    

    def get_pad_postion(
            self,
            pad_name='red_pad',
    ) -> sapien.Pose:
        return get_pose_by_name(self.scene, 'red_pad')
    
    def get_pose_by_name(
            self,
            name:str,
    ) -> sapien.Pose:
        for actor in self.scene.get_all_actors():
            if name==actor.get_name():
                return actor.get_pose()

    def get_names_on_table(self) -> list:
        all_name_list=get_names_in_scene(self.scene)
        graspable_name_list=[]
        for name in all_name_list:
            if "robot" not in name and "pad" not in name and name != "table" and name != "ground":
                graspable_name_list.append(name)
        return graspable_name_list

    def demo(self) -> None:
        while not self.viewer.closed:
            self.scene.update_render()
            self.viewer.render()


if __name__ == '__main__':
    demo = SimplePickPlaceScene()
    demo.demo()
