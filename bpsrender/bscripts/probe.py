import bpy
import os.path as osp

scene = bpy.context.scene
print('BPS:{} {} {}'.format(
    scene.frame_start,
    scene.frame_end,
    osp.splitext(scene.render.filepath)[1]))

