"""
=========================================
Hawkes process with non constant baseline
=========================================

Bla
"""
import numpy as np
import matplotlib.pyplot as plt

from tick.optim.prox import ProxZero

from tick.base import TimeFunction
from tick.plot import plot_timefunction, plot_point_process
from tick.simulation import SimuHawkesSumExpKernels, SimuHawkesMulti
from tick.optim.model import ModelHawkesFixedSumExpKernLeastSq
from tick.optim.solver import AGD

np.random.seed(30923)

period_length = 300
baselines = [[0.3, 0.5, 0.6, 0.4, 0.2, 0],
             [0, 0.5, 0.8, 0.6, 0.2, 0.1]]
n_baselines = len(baselines[0])
decays = [.5, 2., 6.]
adjacency = [[[0, .1, .4], [.2, 0., .2]],
             [[0, 0, 0], [.6, .3, 0]]]

hawkes = SimuHawkesSumExpKernels(baseline=baselines,
                                 period_length=period_length,
                                 decays=decays, adjacency=adjacency,
                                 seed=2093, verbose=False)
hawkes.end_time = 5000
hawkes.adjust_spectral_radius(0.6)

multi = SimuHawkesMulti(hawkes, n_simulations=20)
multi.simulate()

print("n_total_jumps", multi.n_total_jumps)

model = ModelHawkesFixedSumExpKernLeastSq(decays=decays,
                                          n_baselines=n_baselines,
                                          period_length=period_length,
                                          n_threads=4)

model.fit(multi.timestamps)
solver = AGD(step=1e-5, print_every=100, verbose=False, max_iter=1000)
solver.set_model(model).set_prox(ProxZero())
coeffs = solver.solve(0.01 * np.ones(model.n_coeffs))

estimated_baseline1 = coeffs[0:n_baselines]
estimated_baseline2 = coeffs[n_baselines:2 * n_baselines]

print(estimated_baseline1, baselines[0])
print(estimated_baseline2, baselines[1])

t_values_estimated = np.linspace(0, period_length, n_baselines + 1)

_, ax = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

ax[0].step(t_values_estimated, np.hstack((0, estimated_baseline1)),
           label="estimated")
ax[0].step(t_values_estimated, np.hstack((0, baselines[0])), label="original")

ax[1].step(t_values_estimated, np.hstack((0, estimated_baseline2)),
           label="estimated")
ax[1].step(t_values_estimated, np.hstack((0, baselines[1])), label="original")

ax[0].set_ylim(-0.1, ax[0].get_ylim()[1] * 1.2)
ax[0].legend()
ax[1].set_ylim(-0.1, ax[1].get_ylim()[1] * 1.2)
ax[1].legend()
plt.show()
