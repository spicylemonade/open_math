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


def rk4_step(bodies, dt, force_func, **force_kwargs):
    """Classical 4th-order Runge-Kutta integration step.

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
        New body states after one RK4 step.
    """
    n = len(bodies)

    def _make_bodies(state):
        return [Body(bodies[i].mass, state[i][0], state[i][1]) for i in range(n)]

    def _deriv(bs):
        accels = force_func(bs, **force_kwargs)
        return [(bs[i].vel, accels[i]) for i in range(n)]

    def _add_scaled(state, deriv, scale):
        return [
            (Vec2(s[0].x + scale * d[0].x, s[0].y + scale * d[0].y),
             Vec2(s[1].x + scale * d[1].x, s[1].y + scale * d[1].y))
            for s, d in zip(state, deriv)
        ]

    s0 = [(b.pos, b.vel) for b in bodies]

    k1 = _deriv(bodies)
    k2 = _deriv(_make_bodies(_add_scaled(s0, k1, 0.5 * dt)))
    k3 = _deriv(_make_bodies(_add_scaled(s0, k2, 0.5 * dt)))
    k4 = _deriv(_make_bodies(_add_scaled(s0, k3, dt)))

    new_bodies = []
    for i in range(n):
        dx = (k1[i][0].x + 2*k2[i][0].x + 2*k3[i][0].x + k4[i][0].x) * dt / 6.0
        dy = (k1[i][0].y + 2*k2[i][0].y + 2*k3[i][0].y + k4[i][0].y) * dt / 6.0
        dvx = (k1[i][1].x + 2*k2[i][1].x + 2*k3[i][1].x + k4[i][1].x) * dt / 6.0
        dvy = (k1[i][1].y + 2*k2[i][1].y + 2*k3[i][1].y + k4[i][1].y) * dt / 6.0
        new_pos = Vec2(s0[i][0].x + dx, s0[i][0].y + dy)
        new_vel = Vec2(s0[i][1].x + dvx, s0[i][1].y + dvy)
        new_bodies.append(Body(bodies[i].mass, new_pos, new_vel))

    return new_bodies
