# IMPURE
import logging as lg
import os
import os.path as osp
from functools import reduce
from itertools import starmap

from .calls import call
from .commands import get_commands, get_commands_all
from .config import LOGGER, LOGLEV
from .helpers import kickstart


def setup_bspy(cfg, clargs, **kwargs):
    """
    Normalize the names of the script to be ran in Blender for certain steps.
    Eg. the probe step depends on the script located in
    `bpsrender/cfg['probe_py']`.

    Parameters
    ----------
    cfg: dict
    Configuration dictionary.
    clargs: Namespace
    Command line arguments (normalized).
    kwargs: dict

    Returns
    -------
    out: dict
    Dictoinary to be used in call steps.
    """
    out = filter(lambda x: x[0].endswith('_py'), cfg.items())
    out = starmap(lambda k, v: ('{}_normalized'.format(k),
                                osp.join(cfg['bs_path'], v)), out)
    return dict(out)


def setup_probe(cfg, clargs, **kwargs):
    """
    IMPURE
    Call Blender and extract information that will be necessary for later
    steps.

    Parameters
    ----------
    cfg: dict
    Configuration dictionary.
    clargs: Namespace
    Command line arguments (normalized).
    kwargs: dict
    MANDATORY -- see individual functions for the list of mandatory keys
    Dictionary with additional information from the previous setup step.

    Returns
    -------
    out: dict
    Dictoinary to be used in call steps.
    """
    return call(cfg, clargs, get_commands(cfg, clargs, 'probe', **kwargs),
                **kwargs)


def setup_paths(cfg, clargs, **kwargs):
    """
    Figure out appropriate path locations to store output for parts and final
    render.

    Parameters
    ----------
    cfg: dict
    Configuration dictionary.
    clargs: Namespace
    Command line arguments (normalized).
    kwargs: dict
    MANDATORY -- see individual functions for the list of mandatory keys
    Dictionary with additional information from the previous setup step.

    Returns
    -------
    out: dict
    Dictionary storing all relevant information pertaining to folder and file
    paths.

    Note
    ----
    It also creates the folder structure 'render/parts' where
    `clargs.blendfile` is stored on disk.
    """
    render_path = osp.join(osp.dirname(clargs.blendfile), cfg['render_folder'])
    render_parts_path = osp.join(render_path, cfg['parts_folder'])
    name = osp.splitext(osp.basename(clargs.blendfile))[0]
    render_mixdown_path = osp.join(
        render_parts_path, '{}_m.flac'.format(name))
    render_chunk_path = osp.join(
        render_parts_path, '{}_c_{}'.format(name, '#' * cfg['frame_pad']))
    render_video_path = osp.join(
        render_parts_path, '{}_v{}'.format(name, kwargs['ext']))
    render_audiovideo_path = osp.join(
        render_path, '{}{}'.format(name, kwargs['ext']))
    chunks_file_path = osp.join(render_parts_path, cfg['chunks_file'])

    out = {'render_path': render_path,
           'render_parts_path': render_parts_path,
           'chunks_file_path': chunks_file_path,
           'render_chunk_path': render_chunk_path,
           'render_video_path': render_video_path,
           'render_mixdown_path': render_mixdown_path,
           'render_audiovideo_path': render_audiovideo_path}
    return out


def setup_folders_hdd(cfg, clargs, **kwargs):
    """
    IMPURE
    Prepares the folder structure `cfg['render']/cfg['parts']'`.

    Parameters
    ----------
    cfg: dict
    Configuration dictionary.
    clargs: Namespace
    Command line arguments (normalized).
    kwargs: dict
    Dictionary with additional information from the previous setup step.

    Returns
    -------
    out: (iter((str, iter(tuple))), dict)
    1st element: see commands.py:get_commands_all
    2nd elment: the keyword arguments used by calls.py:call
    """
    # create folder structure if it doesn't exist already only if
    # appropriate command line arguments are given
    do_it = filter(lambda x: x[0].endswith('_only'), vars(clargs).items())
    do_it = all(map(lambda x: not x[1], do_it))
    do_it = (not clargs.dry_run
             and clargs.video_only or clargs.mixdown_only or do_it)
    do_it and os.makedirs(kwargs['render_parts_path'], exist_ok=True)
    return {}


def setup(cfg, clargs):
    """
    IMPURE -- setup_paths
    Prepares the folder structure 'render/parts', the appropriate command lists
    to be called and the keyword arguments to be passed to call functions
    (calls.py).

    Parameters
    ----------
    cfg: dict
    Configuration dictionary.
    clargs: Namespace
    Command line arguments (normalized).
    kwargs: dict
    Dictionary with additional information from the previous setup step.

    Returns
    -------
    out: (iter((str, iter(tuple))), dict)
    1st element: see commands.py:get_commands_all
    2nd elment: the keyword arguments used by calls.py:call
    """
    setups_f = (setup_bspy,
                setup_probe,
                setup_paths,
                setup_folders_hdd)
    lg.basicConfig(level=LOGLEV[min(clargs.verbose, len(LOGLEV) - 1)])

    kwargs = dict(reduce(lambda acc, sf: {**acc, **sf(cfg, clargs, **acc)},
                         setups_f, {}))

    LOGGER.info('Setup:')
    kickstart(starmap(lambda k, v:
                      LOGGER.info('{}: {}'.format(k, v)),
                      kwargs.items()))
    return get_commands_all(cfg, clargs, **kwargs), kwargs

