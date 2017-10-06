"""
============================================

This example illustrates the opimization of the model:
    * Logistic regression (`tick.optim.model.ModelLogReg`)

with different solver:
    * SVRG (`tick.optim.solver.SVRG`)
"""

import matplotlib.pyplot as plt
from tick.plot import plot_history
import numpy as np
from itertools import product
from tick.optim.model import ModelLinReg, ModelLogReg, ModelPoisReg
from tick.optim.solver import SDCA, SVRG, BFGS, GD, AGD
from tick.optim.prox import ProxZero, ProxL2Sq
from tick.simulation import SimuLinReg, SimuLogReg, SimuPoisReg

seed = 1398
np.random.seed(seed)

import scipy
from scipy.sparse import csr_matrix

def create_model(model_type, n_samples, n_features, with_intercept=True,
                sparsity=1e-4):
    weights = np.random.randn(n_features)
    intercept = None
    if with_intercept:
        intercept = np.random.normal()

    if model_type == 'Poisson':
        # we need to rescale features to avoid overflows
        weights /= n_features
        if intercept is not None:
            intercept /= n_features

    if model_type == 'Linear':
        simulator = SimuLinReg(weights, intercept=intercept,
                               n_samples=n_samples, verbose=False)
    elif model_type == 'Logistic':
        simulator = SimuLogReg(weights, intercept=intercept,
                               n_samples=n_samples, verbose=False)
    elif model_type == 'Poisson':
        simulator = SimuPoisReg(weights, intercept=intercept,
                                n_samples=n_samples, verbose=False)

    if sparsity < 1:
        labels = (np.random.randint(0, 1, n_samples).astype(float) * 2) - 1
        features = scipy.sparse.rand(n_samples, n_features, density=sparsity, format='csr')
    else:
        features, labels  = simulator.simulate()

    if model_type == 'Linear':
        model = ModelLinReg(fit_intercept=with_intercept)
    elif model_type == 'Logistic':
        model = ModelLogReg(fit_intercept=with_intercept)
    elif model_type == 'Poisson':
        model = ModelPoisReg(fit_intercept=with_intercept)

    model.fit(features, labels)
    return model

def run_solvers(model, l_l2sq):
    try:
        svrg_step = 1. / model.get_lip_max()
    except AttributeError:
        svrg_step = 1e-3
    try:
        gd_step = 1e-1
    except AttributeError:
        gd_step = 1e-1

    # bfgs = BFGS(verbose=False, tol=1e-13)
    # bfgs.set_model(model).set_prox(ProxL2Sq(l_l2sq))
    # bfgs.solve()
    # bfgs.history.set_minimizer(bfgs.solution)
    # bfgs.history.set_minimum(bfgs.objective(bfgs.solution))
    # bfgs.solve()

    asvrg_2 = SVRG(step=svrg_step, verbose=False, seed=seed, threads=2, record_every=1, max_iter=15)
    asvrg_2.set_model(model).set_prox(ProxL2Sq(l_l2sq))
    # asvrg_2.history.set_minimizer(bfgs.solution)
    # asvrg_2.history.set_minimum(bfgs.objective(bfgs.solution))
    asvrg_2.solve()

    asvrg_4 = SVRG(step=svrg_step, verbose=False, seed=seed, threads=4, record_every=1, max_iter=15)
    asvrg_4.set_model(model).set_prox(ProxL2Sq(l_l2sq))
    # asvrg_12.history.set_minimizer(bfgs.solution)
    # asvrg_12.history.set_minimum(bfgs.objective(bfgs.solution))
    asvrg_4.solve()

    asvrg_8 = SVRG(step=svrg_step / 2, verbose=False, seed=seed, threads=8, record_every=1, max_iter=15)
    asvrg_8.set_model(model).set_prox(ProxL2Sq(l_l2sq))
    # asvrg_8.history.set_minimizer(bfgs.solution)
    # asvrg_8.history.set_minimum(bfgs.objective(bfgs.solution))
    asvrg_8.solve()

    svrg  = SVRG(step=svrg_step, verbose=False, seed=seed, record_every=1, max_iter=15)
    svrg.set_model(model).set_prox(ProxL2Sq(l_l2sq))
    # svrg.history.set_minimizer(bfgs.solution)
    # svrg.history.set_minimum(bfgs.objective(bfgs.solution))
    svrg.solve()

    return asvrg_2, asvrg_4, asvrg_8 , svrg


model_types = ['Logistic']
l_l2sqs = [1e-3]

fig, axes = plt.subplots(len(model_types), len(l_l2sqs),
                         figsize=(4 * len(l_l2sqs), 3 * len(model_types)),
                         sharey=True, sharex=True)

axes = np.array([[axes]])

n_samples = 10000
n_features = 20000

for (model_type, l_l2sq), ax in zip(product(model_types, l_l2sqs),
                                    axes.ravel()):
    print("start model")
    model = create_model(model_type, n_samples, n_features)
    print("done model")
    asvrg_2, asvrg_4, asvrg_8, svrg = run_solvers(model, l_l2sq)
    plot_history([asvrg_2, asvrg_4, asvrg_8, svrg], ax=ax, x = "time",
                 dist_min=True, log_scale=True, labels=["ASVRG_2", "ASVRG_4", "ASVRG_8", "SVRG"])
    ax.legend_.remove()
    ax.set_xlabel('')
    ax.set_ylim([1e-9, 1])

for l_l2sq, ax in zip(l_l2sqs, axes[0]):
    ax.set_title('$\lambda = %.2g$' % l_l2sq)

for model_type, ax in zip(model_types, axes):
    ax[0].set_ylabel('%s regression' % model_type, fontsize=17)

for ax in axes[-1]:
    ax.set_xlabel('epochs')

axes[0][0].legend()#loc=9, bbox_to_anchor=(0.5, -0.2), ncol=5)
plt.show()
