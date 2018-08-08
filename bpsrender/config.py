import logging as lg
import multiprocessing as mp
import os.path as osp

CONFIG = {
    'logger': 'BPS',
    'cpu_count': min(int(mp.cpu_count() / 2), 6),
    'bs_path': osp.join(osp.dirname(osp.abspath(__file__)), 'bscripts'),
    'frame_pad': 7,
    'render_folder': 'render',
    'parts_folder': 'parts',
    'chunks_file': 'chunks.txt',
    'video_file': 'video{}',
    'pre': {'work': '»',
            'done': '•',
            'skip': '~'},
    'probe_py': 'probe.py',
    'mixdown_py': 'mixdown.py',
    'video_py': 'video.py'}

LOGGER = lg.getLogger(CONFIG['logger'])
LOGLEV = [lg.INFO, lg.DEBUG]
LOGLEV = [None] + sorted(LOGLEV, reverse=True)

