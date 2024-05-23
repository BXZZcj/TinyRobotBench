"""Create actors (rigid bodies).

The actor (or rigid body) in Sapien is created through a sapien.ActorBuilder.
An actor consists of both collision shapes (for physical simulation) and visual shapes (for rendering).
Note that an actor can have multiple collision and visual shapes,
and they do not need to correspond.

Concepts:
    - Create sapien.Actor by primitives (box, sphere, capsule)
    - Create sapien.Actor by mesh files
    - sapien.Pose
"""

import sapien.core as sapien
from sapien.utils import Viewer
import numpy as np

from config import *


def create_box(
        scene: sapien.Scene,
        pose: sapien.Pose,
        half_size=[0.05, 0.05, 0.05],
        color=[1., 0., 0.],
        name='',
) -> sapien.Actor:
    """Create a box.

    Args:
        scene: sapien.Scene to create a box.
        pose: 6D pose of the box.
        half_size: [3], half size along x, y, z axes.
        color: [3] or [4], rgb or rgba
        name: name of the actor.

    Returns:
        sapien.Actor
    """
    half_size = np.array(half_size)
    builder: sapien.ActorBuilder = scene.create_actor_builder()
    builder.add_box_collision(half_size=half_size)  # Add collision shape
    builder.add_box_visual(half_size=half_size, color=color)  # Add visual shape
    box: sapien.Actor = builder.build(name=name)
    # Or you can set_name after building the actor
    # box.set_name(name)
    box.set_pose(pose)
    return box


def create_sphere(
        scene: sapien.Scene,
        pose: sapien.Pose,
        radius=0.05,
        color=[0., 1., 0.],
        name='',
) -> sapien.Actor:
    """Create a sphere. See create_box."""
    builder = scene.create_actor_builder()
    builder.add_sphere_collision(radius=radius)
    builder.add_sphere_visual(radius=radius, color=color)
    sphere = builder.build(name=name)
    sphere.set_pose(pose)
    return sphere


def create_capsule(
        scene: sapien.Scene,
        pose: sapien.Pose,
        radius=0.05,
        half_length=0.05,
        color=[0., 0., 1.],
        name='',
) -> sapien.Actor:
    """Create a capsule (x-axis <-> half_length). See create_box."""
    builder = scene.create_actor_builder()
    builder.add_capsule_collision(radius=radius, half_length=half_length)
    builder.add_capsule_visual(radius=radius, half_length=half_length, color=color)
    capsule = builder.build(name=name)
    capsule.set_pose(pose)
    return capsule


def create_table(
        scene: sapien.Scene,
        pose: sapien.Pose,
        size=1.0,
        height=1.0,
        thickness=0.1,
        color=(0.8, 0.6, 0.4),
        name='table',
) -> sapien.Actor:
    """Create a table (a collection of collision and visual shapes)."""
    builder = scene.create_actor_builder()
    
    # Tabletop
    tabletop_pose = sapien.Pose([0., 0., -thickness / 2])  # Make the top surface's z equal to 0
    tabletop_half_size = [size / 2, size / 2, thickness / 2]
    builder.add_box_collision(pose=tabletop_pose, half_size=tabletop_half_size)
    builder.add_box_visual(pose=tabletop_pose, half_size=tabletop_half_size, color=color)
    
    # Table legs (x4)
    for i in [-1, 1]:
        for j in [-1, 1]:
            x = i * (size - thickness) / 2
            y = j * (size - thickness) / 2
            table_leg_pose = sapien.Pose([x, y, -height / 2])
            table_leg_half_size = [thickness / 2, thickness / 2, height / 2]
            builder.add_box_collision(pose=table_leg_pose, half_size=table_leg_half_size)
            builder.add_box_visual(pose=table_leg_pose, half_size=table_leg_half_size, color=color)

    table = builder.build_kinematic(name=name)
    table.set_pose(pose)
    return table

def load_object_mesh(
        scene: sapien.Scene,
        pose: sapien.Pose,
        collision_file_path: str,
        visual_file_path: str,
        name='',
) -> sapien.Actor:
    builder = scene.create_actor_builder()
    builder.add_collision_from_file(filename=collision_file_path)
    builder.add_visual_from_file(filename=visual_file_path)

    mesh = builder.build(name=name)
    mesh.set_pose(pose)
    return mesh


def main():
    engine = sapien.Engine()
    renderer = sapien.SapienRenderer()
    engine.set_renderer(renderer)

    scene = engine.create_scene()
    scene.set_timestep(1 / 100.0)

    # ---------------------------------------------------------------------------- #
    # Add actors
    # ---------------------------------------------------------------------------- #
    scene.add_ground(altitude=0)  # The ground is in fact a special actor.
    box = create_box(
        scene,
        sapien.Pose(p=[0, 0, 1.0 + 0.05]),
        half_size=[0.05, 0.05, 0.05],
        color=[1., 0., 0.],
        name='box',
    )
    sphere = create_sphere(
        scene,
        sapien.Pose(p=[0, -0.2, 1.0 + 0.05]),
        radius=0.05,
        color=[0., 1., 0.],
        name='sphere',
    )
    capsule = create_capsule(
        scene,
        sapien.Pose(p=[0, 0.2, 1.0 + 0.05]),
        radius=0.05,
        half_length=0.05,
        color=[0., 0., 1.],
        name='capsule',
    )
    table = create_table(
        scene,
        sapien.Pose(p=[0, 0, 1.0]),
        size=1.0,
        height=1.0,
    )

    # add a mesh
    mesh = load_object_mesh(
        scene, 
        sapien.Pose(p=[-0.2, 0, 1.0 + 0.05]), 
        collision_file_path=manipulate_root_path+'assets/object/banana/collision_meshes/collision.obj',
        visual_file_path=manipulate_root_path+'assets/object/banana/visual_meshes/visual.dae',
        name='mesh',
        )
    

    # ---------------------------------------------------------------------------- #


    scene.set_ambient_light([0.5, 0.5, 0.5])
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])

    viewer = Viewer(renderer)
    viewer.set_scene(scene)

    viewer.set_camera_xyz(x=-2, y=0, z=2.5)
    viewer.set_camera_rpy(r=0, p=-np.arctan2(2, 2), y=0)
    viewer.window.set_camera_parameters(near=0.05, far=100, fovy=1)

    while not viewer.closed:
        scene.step()
        scene.update_render()
        viewer.render()


if __name__ == '__main__':
    main()