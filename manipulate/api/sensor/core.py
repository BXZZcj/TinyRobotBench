import sapien.core as sapien
import numpy as np


def get_pose_by_name(
        scene:sapien.Scene,
        name:str,
) -> sapien.Pose:
    for actor in scene.get_all_actors():
        if name==actor.get_name():
            return actor.get_pose()


def get_names_in_scene(
        scene: sapien.Scene,
) -> list:
    name_list=[]
    for actor in scene.get_all_actors():
        name_list.append(actor.get_name())
    return name_list