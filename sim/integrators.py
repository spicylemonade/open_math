"""Time integration methods for N-body simulation.

All integrators advance the system by one time step dt.
They take (masses, positions, velocities, dt, force_func, **kwargs)
and return updated (positions, velocities).

force_func signature: force_func(masses, positions, **kwargs) -> accelerations
"""

import numpy as np
from sim.forces import direct_summation


def euler(masses, positions, velocities, dt, force_func=direct_summation, **kwargs):
    """Forward Euler integrator (1st order, non-symplectic).

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    dt : float
        Time step.
    force_func : callable
        Function computing accelerations from (masses, positions, **kwargs).
    **kwargs : dict
        Extra arguments passed to force_func (e.g., softening).

    Returns
    -------
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    """
    acc = force_func(masses, positions, **kwargs)
    new_positions = positions + velocities * dt
    new_velocities = velocities + acc * dt
    return new_positions, new_velocities


def leapfrog_kdk(masses, positions, velocities, dt, force_func=direct_summation,
                 acc_prev=None, **kwargs):
    """Leapfrog (kick-drift-kick) integrator (2nd order, symplectic).

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    dt : float
    force_func : callable
    acc_prev : ndarray or None
        Acceleration at current positions. If None, computed from positions.
    **kwargs : dict

    Returns
    -------
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    acc_new : ndarray, shape (N, dim)
        Acceleration at new positions (can be reused as acc_prev in next step).
    """
    if acc_prev is None:
        acc_prev = force_func(masses, positions, **kwargs)

    # Kick (half step)
    vel_half = velocities + 0.5 * dt * acc_prev
    # Drift (full step)
    new_positions = positions + dt * vel_half
    # Compute new acceleration
    acc_new = force_func(masses, new_positions, **kwargs)
    # Kick (half step)
    new_velocities = vel_half + 0.5 * dt * acc_new

    return new_positions, new_velocities, acc_new


def velocity_verlet(masses, positions, velocities, dt, force_func=direct_summation,
                    acc_prev=None, **kwargs):
    """Velocity Verlet integrator (2nd order, symplectic).

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    dt : float
    force_func : callable
    acc_prev : ndarray or None
        Acceleration at current positions.
    **kwargs : dict

    Returns
    -------
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    acc_new : ndarray, shape (N, dim)
    """
    if acc_prev is None:
        acc_prev = force_func(masses, positions, **kwargs)

    # Update positions
    new_positions = positions + velocities * dt + 0.5 * acc_prev * dt * dt
    # Compute new acceleration
    acc_new = force_func(masses, new_positions, **kwargs)
    # Update velocities
    new_velocities = velocities + 0.5 * (acc_prev + acc_new) * dt

    return new_positions, new_velocities, acc_new
