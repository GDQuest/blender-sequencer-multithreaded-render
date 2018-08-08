from collections import deque


class BSError(Exception):
    """
    Custom Exception raised if Blender is called with a python script argument
    and gives error while trying to execute the script.
    """
    pass


def checkblender(what, search, cp, s):
    """
    IMPURE
    Check Blender output for python script execution error.

    Parameters
    ----------
    what: str
    A tag used in the exception message.
    search: str
    The string to search for in Blender's output.
    cp: Popen
    Blender subprocess.
    s: PIPE
    Blender's output.

    Returns
    -------
    out: PIPE
    The same pipe `s` is returned so that it can be iterated over on later
    steps.
    """
    if search in s:
        message = ('Script {what} was not properly executed in'
                   ' Blender'.format(what=what),
                   'CMD: {cmd}'.format(what=what, cmd=' '.join(cp.args)),
                   'DUMP:'.format(what=what), s)
        raise BSError('\n'.join(message))
    return s


def printw(cfg, text, s='\n', e='...', p='', **kwargs):
    p = p or cfg['pre']['work']
    print('{s}{p} {}{e}'.format(text, s=s, e=e, p=p), **kwargs)


def printd(cfg, text, s='', e='.', p='', **kwargs):
    p = p or cfg['pre']['done']
    printw(cfg, text, s=s, e=e, p=p, **kwargs)


def prints(cfg, text, s='', e='.', p='', **kwargs):
    p = p or cfg['pre']['skip']
    printw(cfg, text, s=s, e=e, p=p, **kwargs)


def kickstart(it):
    deque(it, maxlen=0)

