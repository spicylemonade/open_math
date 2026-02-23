"""Adaptive time-stepping controller for N-body simulation.

Implements acceleration-based adaptive time-step selection:
  dt = eta * sqrt(epsilon / |a_max|)
where eta is the accuracy parameter, epsilon is the softening length,
and |a_max| is the maximum acceleration magnitude.

For unsoftened simulations, uses the minimum pairwise distance instead:
  dt = eta * sqrt(r_min^3 / M)
which approximates the local dynamical time.
"""

import numpy as np
from sim.forces import direct_summation


def adaptive_dt(masses, positions, velocities, eta=0.01, dt_min=1e-8, dt_max=0.1,
                softening=0.0, force_func=direct_summation, **kwargs):
    """Compute adaptive time step based on acceleration magnitude.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    eta : float
        Accuracy parameter (dimensionless). Smaller = more accurate.
    dt_min : float
        Minimum allowed time step.
    dt_max : float
        Maximum allowed time step.
    softening : float
        Softening length.
    force_func : callable
    **kwargs : dict

    Returns
    -------
    float
        Recommended time step.
    """
    acc = force_func(masses, positions, softening=softening, **kwargs)
    a_max = np.max(np.linalg.norm(acc, axis=1))

    if a_max < 1e-30:
        return dt_max

    # Use minimum pairwise distance for the length scale
    n = len(masses)
    r_min = np.inf
    for i in range(n):
        for j in range(i + 1, n):
            dr = positions[j] - positions[i]
            r = np.sqrt(np.dot(dr, dr))
            if r < r_min:
                r_min = r

    # dt ~ eta * sqrt(r_min / a_max) (dynamical time estimate)
    dt = eta * np.sqrt(r_min / a_max)
    return np.clip(dt, dt_min, dt_max)


def run_adaptive(masses, positions, velocities, t_end, integrator_step,
                 eta=0.01, dt_min=1e-8, dt_max=0.1, softening=0.0,
                 force_func=direct_summation, **kwargs):
    """Run simulation with adaptive time-stepping.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    t_end : float
        Total simulation time.
    integrator_step : callable
        Integration step function (e.g., leapfrog_kdk).
    eta : float
        Accuracy parameter for adaptive dt.
    dt_min, dt_max : float
    softening : float
    force_func : callable
    **kwargs : dict

    Returns
    -------
    dict with 't', 'positions', 'velocities', 'dt_history', 'n_steps'
    """
    t = 0.0
    pos = positions.copy()
    vel = velocities.copy()
    acc = None
    n_steps = 0
    dt_history = []

    while t < t_end:
        dt = adaptive_dt(masses, pos, vel, eta=eta, dt_min=dt_min, dt_max=dt_max,
                        softening=softening, force_func=force_func)
        # Don't overshoot
        if t + dt > t_end:
            dt = t_end - t

        result = integrator_step(masses, pos, vel, dt, force_func=force_func,
                                 acc_prev=acc, softening=softening, **kwargs)
        pos, vel, acc = result
        t += dt
        n_steps += 1
        dt_history.append(dt)

    return {
        'positions': pos,
        'velocities': vel,
        't': t,
        'dt_history': dt_history,
        'n_steps': n_steps,
    }
