from scene import *
from api import *


scene=SimplePickPlaceScene()
get_names_on_table=scene.get_names_on_table
get_location_by_name=scene.get_pose_by_name
get_pad_position=scene.get_pad_postion
move_tool=scene.grasp_tool.move_for_grasp
grasp=scene.grasp_tool.grasp
ungrasp=scene.grasp_tool.ungrasp


def plan():
    table_objects = get_names_on_table()
    target_box_position = get_pad_position()

    for obj_name in table_objects:
        obj_location = get_location_by_name(obj_name)

        move_tool(obj_location)
        grasp()
        move_tool(target_box_position)
        ungrasp()