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
from .inference import (HawkesADM4, HawkesExpKern, HawkesSumExpKern,
                        HawkesBasisKernels, HawkesConditionalLaw, HawkesEM,
                        HawkesSumGaussians, HawkesCumulantMatching,
                        HawkesCumulantMatchingTf, HawkesCumulantMatchingPyT
                        )

__all__ = [
    "HawkesADM4",
    "HawkesExpKern",
    "HawkesSumExpKern",
    "HawkesBasisKernels",
    "HawkesConditionalLaw",
    "HawkesEM",
    "HawkesSumGaussians",
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
    "HawkesCumulantMatching",
    "HawkesCumulantMatchingTf",
    "HawkesCumulantMatchingPyT",
]

if ModelHawkesExpKernLogLik is not None:
    __all__.extend([
        "ModelHawkesExpKernLogLik",
        "ModelHawkesExpKernLeastSq",
        "ModelHawkesSumExpKernLogLik",
        "ModelHawkesSumExpKernLeastSq",
    ])
