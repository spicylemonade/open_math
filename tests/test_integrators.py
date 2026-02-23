"""Unit tests for Euler and Leapfrog integrators."""

import math
import pytest
from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.integrators import euler_step, leapfrog_step


# --- Helper: constant acceleration force function ---
def constant_accel(bodies, ax=0.0, ay=-1.0, **kwargs):
    """Returns constant acceleration (like uniform gravity) for testing."""
    return [Vec2(ax, ay) for _ in bodies]


def zero_force(bodies, **kwargs):
    """Zero force: free particles."""
    return [Vec2(0, 0) for _ in bodies]


# === Euler tests ===

def test_euler_free_particle():
    """Free particle with constant velocity moves linearly."""
    b = Body(1.0, Vec2(0, 0), Vec2(1, 0))
    result = euler_step([b], 1.0, zero_force)
    assert abs(result[0].pos.x - 1.0) < 1e-10
    assert abs(result[0].pos.y) < 1e-10


def test_euler_constant_accel_position():
    """Under constant acceleration, x = x0 + v0*dt."""
    b = Body(1.0, Vec2(0, 0), Vec2(0, 0))
    result = euler_step([b], 1.0, constant_accel)
    # Euler: new_pos = old_pos + old_vel * dt = (0,0), new_vel = old_vel + a*dt = (0,-1)
    assert abs(result[0].pos.x) < 1e-10
    assert abs(result[0].pos.y) < 1e-10  # pos hasn't moved yet (Euler lag)


def test_euler_constant_accel_velocity():
    """Under constant acceleration, v = v0 + a*dt."""
    b = Body(1.0, Vec2(0, 0), Vec2(0, 0))
    result = euler_step([b], 1.0, constant_accel)
    assert abs(result[0].vel.x) < 1e-10
    assert abs(result[0].vel.y - (-1.0)) < 1e-10


def test_euler_does_not_mutate():
    """Euler should return new bodies, not modify originals."""
    b = Body(1.0, Vec2(0, 0), Vec2(1, 0))
    original_pos = b.pos
    euler_step([b], 1.0, zero_force)
    assert b.pos == original_pos


def test_euler_multiple_bodies():
    """Euler handles multiple bodies."""
    bodies = [
        Body(1.0, Vec2(0, 0), Vec2(1, 0)),
        Body(1.0, Vec2(10, 0), Vec2(-1, 0)),
    ]
    result = euler_step(bodies, 1.0, zero_force)
    assert abs(result[0].pos.x - 1.0) < 1e-10
    assert abs(result[1].pos.x - 9.0) < 1e-10


# === Leapfrog tests ===

def test_leapfrog_free_particle():
    """Free particle with constant velocity moves linearly."""
    b = Body(1.0, Vec2(0, 0), Vec2(1, 0))
    result = leapfrog_step([b], 1.0, zero_force)
    assert abs(result[0].pos.x - 1.0) < 1e-10
    assert abs(result[0].pos.y) < 1e-10


def test_leapfrog_constant_accel_position():
    """Under constant acceleration a, leapfrog gives exact x = x0 + v0*dt + 0.5*a*dt^2."""
    b = Body(1.0, Vec2(0, 0), Vec2(0, 0))
    dt = 1.0
    result = leapfrog_step([b], dt, constant_accel)
    # Exact: y = 0 + 0 + 0.5*(-1)*1 = -0.5
    assert abs(result[0].pos.y - (-0.5)) < 1e-10


def test_leapfrog_constant_accel_velocity():
    """Under constant acceleration, leapfrog gives exact v = v0 + a*dt."""
    b = Body(1.0, Vec2(0, 0), Vec2(0, 0))
    result = leapfrog_step([b], 1.0, constant_accel)
    assert abs(result[0].vel.y - (-1.0)) < 1e-10


def test_leapfrog_does_not_mutate():
    """Leapfrog should return new bodies, not modify originals."""
    b = Body(1.0, Vec2(0, 0), Vec2(1, 0))
    original_pos = b.pos
    leapfrog_step([b], 1.0, zero_force)
    assert b.pos == original_pos


def test_leapfrog_more_accurate_than_euler():
    """For a known problem, leapfrog should be more accurate than Euler after many steps."""
    # Two-body circular orbit: exact position returns to start after one period
    # Use a simpler test: projectile under constant gravity
    b = Body(1.0, Vec2(0, 0), Vec2(1, 0))
    dt = 0.01
    n_steps = 100  # total time = 1.0

    # Euler integration
    bodies_euler = [b]
    for _ in range(n_steps):
        bodies_euler = euler_step(bodies_euler, dt, constant_accel)

    # Leapfrog integration
    bodies_lf = [b]
    for _ in range(n_steps):
        bodies_lf = leapfrog_step(bodies_lf, dt, constant_accel)

    # Exact: x=1.0, y=-0.5 at t=1.0
    err_euler = abs(bodies_euler[0].pos.y - (-0.5))
    err_lf = abs(bodies_lf[0].pos.y - (-0.5))

    # Leapfrog should be exact for constant acceleration
    assert err_lf < 1e-10
    # Euler should have some error
    assert err_euler > err_lf


def test_leapfrog_with_gravity():
    """Leapfrog with gravitational force produces plausible circular orbit behavior."""
    # Set up a circular orbit: two equal masses, center of mass at origin
    # m1 = m2 = 0.5, separation = 2, v = sqrt(G*M/(4*r)) for each body
    m = 0.5
    r = 1.0
    v = math.sqrt(1.0 / (4.0 * r))  # G=1, M=1
    bodies = [
        Body(m, Vec2(r, 0), Vec2(0, v)),
        Body(m, Vec2(-r, 0), Vec2(0, -v)),
    ]

    dt = 0.01
    for _ in range(100):
        bodies = leapfrog_step(bodies, dt, direct_gravity, G=1.0, softening=0.0)

    # Bodies should still be roughly distance 2 apart
    dist = bodies[0].pos.distance_to(bodies[1].pos)
    assert 1.5 < dist < 2.5
