import bpy

EXT = {
    'AVI_JPEG': '.avi',
    'AVI_RAW': '.avi',
    'FFMPEG': {
        'MKV': '.mkv',
        'OGG': '.ogv',
        'QUICKTIME': '.mov',
        'AVI': '.avi',
        'MPEG4': '.mp4'
    }
}

scene = bpy.context.scene

ext = EXT.get(scene.render.image_settings.file_format, 'UNDEFINED')
if scene.render.image_settings.file_format == 'FFMPEG':
    ext = ext[scene.render.ffmpeg.format]
print('\nBPS:{} {} {}\n'.format(scene.frame_start, scene.frame_end, ext))

