# License: BSD 3 clause


def _set_mpl_backend():
    """Make sure that we don't get DISPLAY problems when running without X
    on unices
    Code imported from nilearn (nilearn/nilearn/plotting/__init__.py)
    """
    # We are doing local imports here to avoid polluting our namespace
    try:
        import matplotlib
    except ModuleNotFoundError as exc:
        if exc.name != 'matplotlib':
            raise
        return
    import os
    import sys
    # Set the backend to a non-interactive one for unices without X
    if ((os.name == 'posix' and 'DISPLAY' not in os.environ
         and not (sys.platform == 'darwin'
                  and matplotlib.get_backend() == 'MacOSX'))
            or 'DISPLAY' in os.environ and os.environ['DISPLAY'] == '-1'):
        matplotlib.use('Agg')


_set_mpl_backend()

from tick.array import *
from .timefunc import TimeFunction
from .base import Base
try:
    from ..random import *
except ModuleNotFoundError as exc:
    if exc.name not in {
            'tick.random',
            'tick.random.build',
            'tick.random.build.crandom',
    }:
        raise
from .decorators import actual_kwargs
from .threadpool import ThreadPool

__all__ = ["Base", "TimeFunction", "actual_kwargs"]
