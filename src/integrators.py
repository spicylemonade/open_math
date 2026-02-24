"""
Numerical integration schemes for N-body gravitational simulation.

Implements: Forward Euler, Leapfrog (KDK), Velocity Verlet, and adaptive time-stepping.
"""

import numpy as np
from src.force import compute_accelerations


def forward_euler(masses, positions, velocities, dt, G=1.0, softening=0.0):
    """
    Forward Euler integrator (1st order, non-symplectic).

    x(t+dt) = x(t) + v(t) * dt
    v(t+dt) = v(t) + a(t) * dt
    """
    acc, _ = compute_accelerations(masses, positions, G=G, softening=softening)
    new_pos = positions + velocities * dt
    new_vel = velocities + acc * dt
    return new_pos, new_vel


def leapfrog_kdk(masses, positions, velocities, dt, G=1.0, softening=0.0, acc_prev=None):
    """
    Leapfrog Kick-Drift-Kick symplectic integrator (2nd order).

    1. Half-kick: v(t + dt/2) = v(t) + a(t) * dt/2
    2. Drift: x(t + dt) = x(t) + v(t + dt/2) * dt
    3. Compute a(t + dt)
    4. Half-kick: v(t + dt) = v(t + dt/2) + a(t + dt) * dt/2

    Parameters
    ----------
    acc_prev : ndarray or None - Accelerations from previous step (avoids recomputation)

    Returns
    -------
    new_pos, new_vel, acc_new
    """
    if acc_prev is None:
        acc_prev, _ = compute_accelerations(masses, positions, G=G, softening=softening)

    # Half-kick
    vel_half = velocities + acc_prev * (dt / 2.0)
    # Drift
    new_pos = positions + vel_half * dt
    # Compute new accelerations
    acc_new, _ = compute_accelerations(masses, new_pos, G=G, softening=softening)
    # Half-kick
    new_vel = vel_half + acc_new * (dt / 2.0)

    return new_pos, new_vel, acc_new


def velocity_verlet(masses, positions, velocities, dt, G=1.0, softening=0.0, acc_prev=None):
    """
    Velocity Verlet integrator (2nd order, symplectic).
    Mathematically equivalent to KDK Leapfrog.

    1. x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
    2. Compute a(t+dt)
    3. v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt

    Returns
    -------
    new_pos, new_vel, acc_new
    """
    if acc_prev is None:
        acc_prev, _ = compute_accelerations(masses, positions, G=G, softening=softening)

    # Position update
    new_pos = positions + velocities * dt + 0.5 * acc_prev * dt**2
    # Compute new accelerations
    acc_new, _ = compute_accelerations(masses, new_pos, G=G, softening=softening)
    # Velocity update
    new_vel = velocities + 0.5 * (acc_prev + acc_new) * dt

    return new_pos, new_vel, acc_new


def run_simulation(masses, positions, velocities, dt, n_steps, integrator='leapfrog',
                   G=1.0, softening=0.0, store_every=1):
    """
    Run an N-body simulation for n_steps.

    Parameters
    ----------
    integrator : str - 'euler', 'leapfrog', or 'verlet'
    store_every : int - Store state every N steps

    Returns
    -------
    dict with keys: 'times', 'positions', 'velocities'
        positions/velocities are lists of arrays stored at each output step
    """
    times = [0.0]
    pos_history = [positions.copy()]
    vel_history = [velocities.copy()]

    pos = positions.copy()
    vel = velocities.copy()
    t = 0.0

    # Pre-compute initial accelerations for leapfrog/verlet
    acc = None
    if integrator in ('leapfrog', 'verlet'):
        acc, _ = compute_accelerations(masses, pos, G=G, softening=softening)

    for step in range(1, n_steps + 1):
        if integrator == 'euler':
            pos, vel = forward_euler(masses, pos, vel, dt, G=G, softening=softening)
        elif integrator == 'leapfrog':
            pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt, G=G, softening=softening, acc_prev=acc)
        elif integrator == 'verlet':
            pos, vel, acc = velocity_verlet(masses, pos, vel, dt, G=G, softening=softening, acc_prev=acc)
        else:
            raise ValueError(f"Unknown integrator: {integrator}")

        t += dt

        if step % store_every == 0:
            times.append(t)
            pos_history.append(pos.copy())
            vel_history.append(vel.copy())

    return {
        'times': np.array(times),
        'positions': pos_history,
        'velocities': vel_history,
        'masses': masses,
    }


def run_simulation_adaptive(masses, positions, velocities, dt_init, t_end,
                            G=1.0, softening=0.0, eta=0.01, dt_min=1e-10,
                            dt_max=0.1, store_every=1):
    """
    Run simulation with adaptive time-stepping based on acceleration magnitude.
    Uses leapfrog KDK as base integrator.

    dt = eta * sqrt(softening / |a_max|) if softening > 0
    dt = eta * min(|v_i| / |a_i|) otherwise (bounded by dt_min, dt_max)

    Returns
    -------
    dict with keys: 'times', 'positions', 'velocities', 'dt_history', 'total_steps'
    """
    times = [0.0]
    pos_history = [positions.copy()]
    vel_history = [velocities.copy()]
    dt_history = []

    pos = positions.copy()
    vel = velocities.copy()
    t = 0.0
    total_steps = 0

    acc, _ = compute_accelerations(masses, pos, G=G, softening=softening)

    store_counter = 0

    while t < t_end:
        # Compute adaptive timestep
        a_mag = np.sqrt(np.sum(acc ** 2, axis=1))
        a_max = np.max(a_mag)

        if a_max > 0:
            if softening > 0:
                dt = eta * np.sqrt(softening / a_max)
            else:
                # Use minimum pairwise timescale
                dt = eta / np.sqrt(a_max)
        else:
            dt = dt_init

        dt = np.clip(dt, dt_min, dt_max)

        # Don't overshoot t_end
        if t + dt > t_end:
            dt = t_end - t

        # Leapfrog step
        pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt, G=G, softening=softening, acc_prev=acc)
        t += dt
        total_steps += 1
        store_counter += 1
        dt_history.append(dt)

        if store_counter >= store_every:
            times.append(t)
            pos_history.append(pos.copy())
            vel_history.append(vel.copy())
            store_counter = 0

    return {
        'times': np.array(times),
        'positions': pos_history,
        'velocities': vel_history,
        'masses': masses,
        'dt_history': np.array(dt_history),
        'total_steps': total_steps,
    }
