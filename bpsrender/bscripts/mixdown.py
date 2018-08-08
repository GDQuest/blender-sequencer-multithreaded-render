import bpy
import os.path as osp
import sys


for strip in bpy.context.scene.sequence_editor.sequences_all:
    if strip.type == 'META':
        continue
    if strip.type != 'SOUND':
        strip.mute = True

path = sys.argv[-1]
ext = osp.splitext(path)[1][1:].upper()
bpy.ops.sound.mixdown(
    filepath=path,
    check_existing=False,
    container=ext,
    codec=ext)

