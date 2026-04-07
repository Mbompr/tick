# License: BSD 3 clause

import tick.base
import tick.linear_model.build.linear_model

try:
    import tick.robust.build.robust
except ImportError:
    pass

from .gd import GD
from .agd import AGD
from .bfgs import BFGS
from .scpg import SCPG
from .sgd import SGD
from .svrg import SVRG
# Keep imports resilient while the pybind11 migration is in progress.
try:
    from .saga import SAGA
except ImportError:
    SAGA = None
from .sdca import SDCA
from .gfb import GFB
try:
    from .adagrad import AdaGrad
except ImportError:
    AdaGrad = None
from .history import History

__all__ = [
    "GD", "AGD", "BFGS", "SCPG", "SGD", "SVRG", "SAGA", "SDCA", "GFB",
    "AdaGrad", "History"
]
