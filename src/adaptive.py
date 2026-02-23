"""Adaptive time-stepping controller for N-body integration."""

import math
from src.vector import Vec2
from src.body import Body


class AdaptiveController:
    """Adaptive time-step controller based on maximum acceleration magnitude.

    The time step is computed as:
        dt = eta / sqrt(max|a|)

    where eta is a safety parameter and max|a| is the maximum acceleration
    magnitude across all bodies.

    Parameters
    ----------
    eta : float
        Safety/accuracy parameter controlling step size.
    dt_min : float
        Minimum allowed time step.
    dt_max : float
        Maximum allowed time step.
    """

    def __init__(self, eta=0.01, dt_min=1e-8, dt_max=0.1):
        self.eta = eta
        self.dt_min = dt_min
        self.dt_max = dt_max

    def compute_dt(self, accelerations):
        """Compute adaptive time step from current accelerations.

        Parameters
        ----------
        accelerations : list of Vec2
            Current acceleration for each body.

        Returns
        -------
        float
            Adaptive time step.
        """
        max_a = 0.0
        for a in accelerations:
            a_mag = a.magnitude()
            if a_mag > max_a:
                max_a = a_mag

        if max_a < 1e-30:
            return self.dt_max

        dt = self.eta / math.sqrt(max_a)
        return max(self.dt_min, min(self.dt_max, dt))


def adaptive_step(bodies, force_func, integrator, controller, **force_kwargs):
    """Perform one adaptive integration step.

    Parameters
    ----------
    bodies : list of Body
        Current body states.
    force_func : callable
        Force computation function.
    integrator : callable
        Integration step function (e.g., leapfrog_step or rk4_step).
    controller : AdaptiveController
        Adaptive time-step controller.
    **force_kwargs : dict
        Additional keyword arguments for force_func.

    Returns
    -------
    tuple of (list of Body, float)
        New body states and the dt used.
    """
    accelerations = force_func(bodies, **force_kwargs)
    dt = controller.compute_dt(accelerations)
    new_bodies = integrator(bodies, dt, force_func, **force_kwargs)
    return new_bodies, dt


def run_adaptive_simulation(bodies, force_func, integrator, controller,
                            total_time, force_kwargs=None, record_interval=0):
    """Run a simulation with adaptive time-stepping.

    Parameters
    ----------
    bodies : list of Body
        Initial body states.
    force_func : callable
        Force function.
    integrator : callable
        Integrator step function.
    controller : AdaptiveController
        Time-step controller.
    total_time : float
        Total simulation time.
    force_kwargs : dict
        Force function kwargs.
    record_interval : float
        Record state at this interval (0 = every step).

    Returns
    -------
    dict
        Results with times, dt_history, positions, energies.
    """
    if force_kwargs is None:
        force_kwargs = {}

    G = force_kwargs.get('G', 1.0)
    softening = force_kwargs.get('softening', 0.0)
    eps2 = softening * softening

    t = 0.0
    step_count = 0
    dt_history = []
    times = []
    energies = []

    def _compute_energy(bs):
        ke = sum(0.5 * b.mass * b.vel.magnitude_squared() for b in bs)
        pe = 0.0
        n = len(bs)
        for i in range(n):
            for j in range(i + 1, n):
                dx = bs[j].pos.x - bs[i].pos.x
                dy = bs[j].pos.y - bs[i].pos.y
                r = math.sqrt(dx * dx + dy * dy + eps2)
                pe -= G * bs[i].mass * bs[j].mass / r
        return ke + pe

    times.append(t)
    energies.append(_compute_energy(bodies))

    while t < total_time:
        bodies, dt = adaptive_step(bodies, force_func, integrator, controller,
                                   **force_kwargs)
        # Don't overshoot
        if t + dt > total_time:
            dt = total_time - t
            bodies = integrator(bodies, dt, force_func, **force_kwargs)

        t += dt
        step_count += 1
        dt_history.append(dt)
        times.append(t)
        energies.append(_compute_energy(bodies))

    return {
        'bodies': bodies,
        'step_count': step_count,
        'dt_history': dt_history,
        'times': times,
        'energies': energies,
        'final_time': t,
    }
