# License: BSD 3 clause

import tick.base
import tick.base_model.build.base_model

from .model_linreg import ModelLinReg
from .model_logreg import ModelLogReg

from .simu_linreg import SimuLinReg
from .simu_logreg import SimuLogReg

try:
    from .linear_regression import LinearRegression
except ImportError:
    LinearRegression = None

try:
    from .logistic_regression import LogisticRegression
except ImportError:
    LogisticRegression = None

try:
    from .poisson_regression import PoissonRegression
except ImportError:
    PoissonRegression = None

try:
    from .model_poisreg import ModelPoisReg
    from .simu_poisreg import SimuPoisReg
except ImportError:
    ModelPoisReg = None
    SimuPoisReg = None

try:
    from .model_hinge import ModelHinge
except ImportError:
    ModelHinge = None

try:
    from .model_smoothed_hinge import ModelSmoothedHinge
except ImportError:
    ModelSmoothedHinge = None

try:
    from .model_quadratic_hinge import ModelQuadraticHinge
except ImportError:
    ModelQuadraticHinge = None

__all__ = [
    'LinearRegression', 'LogisticRegression', 'LogisticRegression',
    'ModelLinReg', 'ModelLogReg', 'ModelPoisReg', 'ModelHinge',
    'ModelSmoothedHinge', 'ModelQuadraticHinge', 'SimuLinReg', 'SimuLogReg',
    'SimuPoisReg'
]
