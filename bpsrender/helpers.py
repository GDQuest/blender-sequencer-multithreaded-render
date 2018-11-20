from collections import deque
from shutil import which


class BSError(Exception):
    """
    Custom Exception raised if Blender is called with a python script argument
    and gives error while trying to execute the script.
    """
    pass


class ToolError(Exception):
    """Raised if external dependencies aren't found on system.
    """
    pass


def checktools(tools):
    tools = [(t, which(t) or '') for t in tools]
    check = {'tools': tools,
             'test': all(map(lambda x: x[1], tools))}
    if not check['test']:
        msg = ["BPSRender couldn't find external dependencies:"]
        msg += ['[{check}] {tool}: {path}'.format(check='v' if path is not '' else 'X',
                                                  tool=tool, path=path or 'NOT FOUND')
                for tool, path in check['tools']]
        msg += [('Check if you have them properly installed and available in the PATH'
                 ' environemnt variable.'),
                'Exiting...']
        raise ToolError('\n'.join(msg))


def checkblender(what, search, cp, s):
    """
    IMPURE
    Check Blender output for python script execution error.

    Parameters
    ----------
    what: str
    A tag used in the exception message.
    search: iter(str)
    One or more string(s) to search for in Blender's output.
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
    if not isinstance(search, list):
        search = [search]
    for search_item in search:
        if search_item in s:
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

