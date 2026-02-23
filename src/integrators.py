"""Numerical integrators for the N-body simulation."""

from src.body import Body
from src.vector import Vec2


def euler_step(bodies, dt, force_func, **force_kwargs):
    """Forward Euler integration step.

    Parameters
    ----------
    bodies : list of Body
        Current state.
    dt : float
        Time step.
    force_func : callable
        Function(bodies, **kwargs) -> list of Vec2 accelerations.
    **force_kwargs : dict
        Additional keyword arguments passed to force_func.

    Returns
    -------
    list of Body
        New body states after one Euler step.
    """
    accelerations = force_func(bodies, **force_kwargs)
    new_bodies = []
    for b, a in zip(bodies, accelerations):
        new_vel = b.vel + a * dt
        new_pos = b.pos + b.vel * dt
        new_bodies.append(Body(b.mass, new_pos, new_vel))
    return new_bodies


def leapfrog_step(bodies, dt, force_func, **force_kwargs):
    """Kick-Drift-Kick leapfrog (Stormer-Verlet) integration step.

    Parameters
    ----------
    bodies : list of Body
        Current state.
    dt : float
        Time step.
    force_func : callable
        Function(bodies, **kwargs) -> list of Vec2 accelerations.
    **force_kwargs : dict
        Additional keyword arguments passed to force_func.

    Returns
    -------
    list of Body
        New body states after one leapfrog step.
    """
    half_dt = 0.5 * dt

    # Kick: half-step velocity update
    accel_old = force_func(bodies, **force_kwargs)
    kicked = []
    for b, a in zip(bodies, accel_old):
        v_half = b.vel + a * half_dt
        kicked.append(Body(b.mass, b.pos, v_half))

    # Drift: full-step position update
    drifted = []
    for b in kicked:
        new_pos = b.pos + b.vel * dt
        drifted.append(Body(b.mass, new_pos, b.vel))

    # Kick: second half-step velocity update
    accel_new = force_func(drifted, **force_kwargs)
    new_bodies = []
    for b, a in zip(drifted, accel_new):
        new_vel = b.vel + a * half_dt
        new_bodies.append(Body(b.mass, b.pos, new_vel))

    return new_bodies
