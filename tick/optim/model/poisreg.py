
from .build.model import ModelPoisReg as _ModelPoisReg
from .build.model import LinkType_identity as identity
from .build.model import LinkType_exponential as exponential

import numpy as np
from .base import ModelGeneralizedLinear, ModelFirstOrder, ModelSecondOrder, \
    ModelSelfConcordant


__author__ = 'Stephane Gaiffas'


class ModelPoisReg(ModelGeneralizedLinear,
                   ModelSecondOrder,
                   ModelSelfConcordant):
    """Poisson regression model with identity or exponential link.
    This class gives first order and second order information for this
    model (gradient, loss and hessian norm).

    Parameters
    ----------
    fit_intercept : `bool`
        If `True`, the model uses an intercept

    link : `str`, default="exponential"
        Type of link function

        * if ``"identity"``: the intensity is the inner product of the
          model's coeffs with the features. In this case, one
          must ensure that the intensity is non-negative

        * if ``"exponential"``: the intensity is the exponential of the
          inner product of the model's coeffs with the features.

        Note that link cannot be changed after creation of
        `ModelPoisReg`

    Attributes
    ----------
    features : `numpy.ndarray`, shape=(n_samples, n_features) (read-only)
        The features matrix

    labels : `numpy.ndarray`, shape=(n_samples,) (read-only)
        The labels vector

    n_samples : `int` (read-only)
        Number of samples

    n_features : `int` (read-only)
        Number of features

    n_coeffs : `int` (read-only)
        Total number of coefficients of the model

    n_threads : `int`, default=1 (read-only)
        Number of threads used for parallel computation.

        * if ``int <= 0``: the number of physical cores available on
          the CPU
        * otherwise the desired number of threads

    Notes
    -----
    The gradient and loss for the exponential link case cannot be
    overflow proof. In this case, only a solver working in the dual
    (such as `SDCA`) should be used.

    In summary, use grad and call at your own risk when
    ``link="exponential"``
    """

    _attrinfos = {
        "_link_type": {
            "writable": False
        },
        "_link": {
            "writable": False
        }
    }

    def __init__(self, fit_intercept: bool = True,
                 link: str = "exponential", n_threads: int = 1):
        """
        """
        ModelSecondOrder.__init__(self)
        ModelGeneralizedLinear.__init__(self, fit_intercept)
        ModelSelfConcordant.__init__(self)
        self._set("_link", None)
        self.link = link
        self.n_threads = n_threads

    # TODO: implement _set_data and not fit
    def fit(self, features, labels):
        """Set the data into the model object

        Parameters
        ----------
        features : `numpy.ndarray`, shape=(n_samples, n_features)
            The features matrix

        labels : `numpy.ndarray`, shape=(n_samples,)
            The labels vector

        Returns
        -------
        output : `ModelPoisReg`
            The current instance with given data
        """
        ModelFirstOrder.fit(self, features, labels)
        ModelGeneralizedLinear.fit(self, features, labels)
        self._set("_model", _ModelPoisReg(features,
                                          labels,
                                          self._link_type,
                                          self.fit_intercept,
                                          self.n_threads))
        return self

    def _grad(self, coeffs: np.ndarray, out: np.ndarray) -> None:
        self._model.grad(coeffs, out)

    def _loss(self, coeffs: np.ndarray) -> float:
        return self._model.loss(coeffs)

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        if self._link is not None:
            raise ValueError("link is read only")
        if value == "exponential":
            self._set("_link_type", exponential)
        elif value == "identity":
            self._set("_link_type", identity)
        else:
            raise ValueError("``link`` must be either 'exponential' or "
                             "'linear'.")
        self._set("_link", value)

    def _get_sc_constant(self) -> float:
        """Self-concordance parameter of the Poisson
        regression loss
        """
        if self.link == "identity":
            y = self.labels
            return 2 * (1. / np.sqrt(y[y > 0])).max()
        else:
            raise ValueError(("Poisson regression with exponential "
                              "link is not self-concordant"))

    # TODO: C++ for this
    def _hessian_norm(self, coeffs: np.ndarray,
                      point: np.ndarray) -> float:

        link = self.link
        features, labels = self.features, self.labels
        if link == "identity":
            z1 = features.dot(coeffs)
            z2 = features.dot(point)
            # TODO: beware of zeros in z1 or z2 !
            return np.sqrt((labels * z1 ** 2 / z2 ** 2).mean())
        elif link == "exponential":
            raise NotImplementedError("exp link is not yet implemented")
        else:
            raise ValueError("``link`` must be either 'exponential' or "
                             "'linear'.")

