# License: BSD 3 clause

try:
    from .model import (
        ModelHawkesExpKernLogLik,
        ModelHawkesExpKernLeastSq,
        ModelHawkesSumExpKernLogLik,
        ModelHawkesSumExpKernLeastSq,
    )
except ImportError:
    ModelHawkesExpKernLogLik = None
    ModelHawkesExpKernLeastSq = None
    ModelHawkesSumExpKernLogLik = None
    ModelHawkesSumExpKernLeastSq = None
from .simulation import (SimuPoissonProcess, SimuInhomogeneousPoisson,
                         SimuHawkes, SimuHawkesMulti, SimuHawkesExpKernels,
                         SimuHawkesSumExpKernels, HawkesKernel0,
                         HawkesKernelExp, HawkesKernelPowerLaw,
                         HawkesKernelSumExp, HawkesKernelTimeFunc)
try:
    from .inference import (HawkesADM4, HawkesExpKern, HawkesSumExpKern,
                            HawkesBasisKernels, HawkesConditionalLaw,
                            HawkesEM, HawkesSumGaussians,
                            HawkesCumulantMatching,
                            HawkesCumulantMatchingTf,
                            HawkesCumulantMatchingPyT)
except ImportError:
    HawkesADM4 = None
    HawkesExpKern = None
    HawkesSumExpKern = None
    HawkesBasisKernels = None
    HawkesConditionalLaw = None
    HawkesEM = None
    HawkesSumGaussians = None
    HawkesCumulantMatching = None
    HawkesCumulantMatchingTf = None
    HawkesCumulantMatchingPyT = None

__all__ = [
    "SimuPoissonProcess",
    "SimuInhomogeneousPoisson",
    "SimuHawkes",
    "SimuHawkesMulti",
    "SimuHawkesExpKernels",
    "SimuHawkesSumExpKernels",
    "HawkesKernel0",
    "HawkesKernelExp",
    "HawkesKernelPowerLaw",
    "HawkesKernelSumExp",
    "HawkesKernelTimeFunc",
]

if ModelHawkesExpKernLogLik is not None:
    __all__.extend([
        "ModelHawkesExpKernLogLik",
        "ModelHawkesExpKernLeastSq",
        "ModelHawkesSumExpKernLogLik",
        "ModelHawkesSumExpKernLeastSq",
    ])

if HawkesADM4 is not None:
    __all__.extend([
        "HawkesADM4",
        "HawkesExpKern",
        "HawkesSumExpKern",
        "HawkesBasisKernels",
        "HawkesConditionalLaw",
        "HawkesEM",
        "HawkesSumGaussians",
        "HawkesCumulantMatching",
        "HawkesCumulantMatchingTf",
        "HawkesCumulantMatchingPyT",
    ])
