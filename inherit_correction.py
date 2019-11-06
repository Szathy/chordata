import os
import time

import bpy
from mathutils import *
from math import *

print("=============================")
print("====== GET OBJECTS, INIT ====")

object = bpy.context.object
pose = object.pose.bones
bones = object.data.bones

inherit = False

# INIT
for b in pose:
    b.rotation_quaternion.identity()

for b in bones:
    # SET INHERIT
    b.use_inherit_rotation = inherit

print("====== CREATE POST AND CORRECT IF NEEDED ====")

body_json = {}
body_json["r-forarm"] = {}
body_json["r-arm"] = {}
body_json["r-forarm"]["pose_rot_quat"] = Quaternion((0.6, 0, 0, -0.5))
body_json["r-arm"]["pose_rot_quat"] = Quaternion((-0.9, 0.5, 0.5, 0.7))

if not inherit:
    object.pose.bones["r-arm"].rotation_quaternion = body_json["r-arm"]["pose_rot_quat"]
    object.pose.bones["r-forarm"].rotation_quaternion = body_json["r-forarm"]["pose_rot_quat"]

if inherit:
    object.pose.bones["r-forarm"].rotation_quaternion = body_json["r-forarm"]["pose_rot_quat"]
    object.pose.bones["r-arm"].rotation_quaternion = body_json["r-arm"]["pose_rot_quat"]

    # NOT WOKRING METHOD
    forarm_rot_quat = object.pose.bones["r-forarm"].rotation_quaternion
    rot_diff = Quaternion((1, 0, 0, 0)).rotation_difference(
        forarm_rot_quat).conjugated()
    arm_rot_quat = object.pose.bones["r-arm"].rotation_quaternion.copy()
    arm_local_quat = object.data.bones["r-arm"].matrix_local.to_quaternion().copy()
    q = arm_local_quat.conjugated() * rot_diff.copy().conjugated() * arm_local_quat
    object.pose.bones["r-arm"].rotation_quaternion = q * arm_rot_quat
