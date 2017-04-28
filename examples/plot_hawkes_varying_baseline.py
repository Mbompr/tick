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

n_baselines = 24
period_length = 24
t_values = np.linspace(0, period_length, n_baselines + 1)

y_values1 = 0.1 * np.maximum(np.sin(t_values * 2 * np.pi / period_length) +
                             0.5, 0) + 0.1
baselines_1 = TimeFunction((t_values, y_values1),
                           border_type=TimeFunction.Cyclic,
                           inter_mode=TimeFunction.InterConstRight)

y_values2 = 0.2 * np.maximum(
    np.cos((t_values * 2 * np.pi + 1) / period_length) + 0.2, 0) + 0.2
baselines_2 = TimeFunction((t_values, y_values2),
                           border_type=TimeFunction.Cyclic,
                           inter_mode=TimeFunction.InterConstRight)
# plot_timefunction(baselines_2)

decays = [.5, 2., 6.]
adjacency = [[[0, .1, .4], [.2, 0., .2]],
             [[0, 0, 0], [.6, .3, 0]]]

hawkes = SimuHawkesSumExpKernels(baseline=[baselines_1, baselines_2],
                                 decays=decays, adjacency=adjacency,
                                 seed=2093, verbose=False)
# hawkes.track_intensity(0.1)
hawkes.end_time = 50000
hawkes.adjust_spectral_radius(0.6)

multi = SimuHawkesMulti(hawkes, n_simulations=20)

multi.simulate()

print("n_total_jumps", multi.n_total_jumps)
print("spectral_radius", multi.spectral_radius)

# plot_point_process(hawkes)

model = ModelHawkesFixedSumExpKernLeastSq(decays=decays,
                                          n_baselines=n_baselines,
                                          period_length=period_length,
                                          n_threads=4)

model.fit(multi.timestamps)
solver = AGD(step=1e-5, print_every=100, verbose=True, max_iter=1000)
solver.set_model(model).set_prox(ProxZero())
coeffs = solver.solve(0.01 * np.ones(model.n_coeffs))

estimated_baseline1 = coeffs[0:n_baselines]
estimated_baseline2 = coeffs[n_baselines:2 * n_baselines]

print(estimated_baseline1, y_values1)
print(estimated_baseline2, y_values2)

t_values_estimated = np.linspace(0, period_length, n_baselines + 1)
t_values = np.linspace(0, period_length, 1000)

_, ax = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

estimated_baseline_tf1 = TimeFunction(
    (t_values_estimated, np.hstack((estimated_baseline1, 0))),
    inter_mode=TimeFunction.InterConstRight)
ax[0].plot(t_values, estimated_baseline_tf1.value(t_values),
           label="estimated")
ax[0].plot(t_values, baselines_1.value(t_values), label="original")

estimated_baseline_tf2 = TimeFunction(
    (t_values_estimated, np.hstack((estimated_baseline2, 0))),
    inter_mode=TimeFunction.InterConstRight)
ax[1].plot(t_values, estimated_baseline_tf2.value(t_values),
           label="estimated")
ax[1].plot(t_values, baselines_2.value(t_values), label="original")

ax[0].set_ylim(-0.1, ax[0].get_ylim()[1] * 1.5)
ax[0].legend()
ax[1].set_ylim(-0.1, ax[1].get_ylim()[1] * 1.5)
ax[1].legend()
plt.show()
