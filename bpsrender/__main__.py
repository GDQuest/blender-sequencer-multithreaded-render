"""
Renders videos edited in Blender 3D's Video Sequence Editor using multiple CPU
cores. Original script by Justin Warren:
https://github.com/sciactive/pulverize/blob/master/pulverize.py
Modified by sudopluto (Pranav Sharma), gdquest (Nathan Lovato) and
razcore (Razvan Radulescu)

Under GPLv3 license
"""
import argparse as ap
import os.path as osp
import sys
from functools import partial

from .calls import call
from .config import CONFIG as C
from .helpers import kickstart, prints
from .setup import setup

# https://github.com/mikeycal/the-video-editors-render-script-for-blender#configuring-the-script
# there seems no easy way to grab the ram usage in a mulitplatform way
# without writing platform dependent code, or by using a python module

# Most popluar config is 4 cores, 8 GB ram, this is the default for the script
# https://store.steampowered.com/hwsurvey/


def parse_arguments(cfg):
    """
    Uses `argparse` to parse the command line arguments.

    Parameters
    ----------
    cfg: dict
    Configuration dictionary.

    Returns
    -------
    out: Namespace
    Command line arguments (normalized).
    """
    p = ap.ArgumentParser(
        description='Multi-process Blender VSE rendering - will attempt to'
        ' create a folder called `render` inside of the folder'
        ' containing `blendfile`. Insider `render` another folder called'
        ' `parts` will be created for storing temporary files. These files'
        ' will be joined together as the last step to produce the final'
        ' render which will be stored inside `render` and it will have the'
        ' same name as `blendfile`')
    p.add_argument(
        '-w',
        '--workers',
        type=int,
        default=cfg['cpu_count'],
        help='Number of workers in the pool (for video rendering).')
    p.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='Increase verbosity level (eg. -vvv).')
    p.add_argument(
        '--dry-run',
        action='store_true',
        help=('Run the script without actual rendering or creating files and'
              ' folders. For DEBUGGING purposes'))
    p.add_argument(
        '-m', '--mixdown-only',
        action='store_true',
        help='ONLY render the audio MIXDOWN')
    p.add_argument(
        '-c', '--concatenate-only',
        action='store_true',
        help='ONLY CONCATENATE the (already) available video chunks')
    p.add_argument(
        '-d', '--video-only',
        action='store_true',
        help='ONLY render the VIDEO (implies --concatenate-only).')
    p.add_argument(
        '-j', '--join-only',
        action='store_true',
        help='ONLY JOIN the mixdown with the video. This will produce the'
        ' final render')
    p.add_argument('blendfile', help='Blender project file to render.')

    clargs = p.parse_args()
    clargs.blendfile = osp.abspath(clargs.blendfile)
    # --video-only implies --concatenate-only
    clargs.concatenate_only = clargs.concatenate_only or clargs.video_only
    # --dry-run implies maximum verbosity level
    clargs.verbose = 99999 if clargs.dry_run else clargs.verbose
    return clargs


def main():
    """
    Script entry point.
    """
    try:
        clargs = parse_arguments(C)
        cmds, kwargs = setup(C, clargs)
        kickstart(map(partial(call, C, clargs, **kwargs), cmds))
    except KeyboardInterrupt:
        # TODO: add actual clean up code
        prints(C, 'DirtyInterrupt. Exiting', s='\n\n', e='...')
        sys.exit()


# this is so it can be ran as a module: `python3 -m bpsrender` (for testing)
if __name__ == '__main__':
    main()

