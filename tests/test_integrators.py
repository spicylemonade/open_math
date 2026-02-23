"""Unit tests for Euler and Leapfrog integrators."""

import math
import pytest
from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.integrators import euler_step, leapfrog_step, rk4_step


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


# === RK4 tests ===

def test_rk4_free_particle():
    """Free particle with constant velocity moves linearly."""
    b = Body(1.0, Vec2(0, 0), Vec2(1, 0))
    result = rk4_step([b], 1.0, zero_force)
    assert abs(result[0].pos.x - 1.0) < 1e-10
    assert abs(result[0].pos.y) < 1e-10


def test_rk4_constant_accel_exact():
    """RK4 should be exact for constant acceleration (polynomial of degree <= 3)."""
    b = Body(1.0, Vec2(0, 0), Vec2(0, 0))
    dt = 1.0
    result = rk4_step([b], dt, constant_accel)
    # Exact: y = 0.5*a*t^2 = -0.5, vy = a*t = -1.0
    assert abs(result[0].pos.y - (-0.5)) < 1e-10
    assert abs(result[0].vel.y - (-1.0)) < 1e-10


def test_rk4_does_not_mutate():
    """RK4 should not modify input bodies."""
    b = Body(1.0, Vec2(0, 0), Vec2(1, 0))
    original_pos = b.pos
    rk4_step([b], 1.0, zero_force)
    assert b.pos == original_pos


def test_rk4_fourth_order_convergence():
    """Halving dt should reduce single-step error by ~16x (4th order)."""
    # Use gravitational two-body problem for non-trivial dynamics
    bodies = [
        Body(1.0, Vec2(0, 0), Vec2(0, 0)),
        Body(1e-6, Vec2(1, 0), Vec2(0, 1)),
    ]

    # Reference: very small dt
    dt_ref = 0.0001
    ref = rk4_step(bodies, dt_ref, direct_gravity, G=1.0, softening=0.0)

    # Two steps with dt
    dt1 = 0.01
    dt2 = dt1 / 2.0

    # Single step with dt1
    result1 = rk4_step(bodies, dt1, direct_gravity, G=1.0, softening=0.0)

    # Single step with dt2
    result2 = rk4_step(bodies, dt2, direct_gravity, G=1.0, softening=0.0)

    # Compare to reference at their respective times (not the same time, so
    # compare truncation errors). For order p, error ~ C*dt^(p+1).
    # Since we're doing single steps starting from the same IC:
    # err(dt) ~ C * dt^5 for RK4
    # err(dt/2) ~ C * (dt/2)^5 = err(dt)/32

    # Actually, for a single step the local truncation error is O(dt^5).
    # Let's use a simpler approach: integrate the same total time with N and 2N steps.
    total_time = 0.1
    n1 = 10
    n2 = 20
    dt1 = total_time / n1
    dt2 = total_time / n2

    b1 = list(bodies)
    for _ in range(n1):
        b1 = rk4_step(b1, dt1, direct_gravity, G=1.0, softening=0.0)

    b2 = list(bodies)
    for _ in range(n2):
        b2 = rk4_step(b2, dt2, direct_gravity, G=1.0, softening=0.0)

    # Reference with very fine dt
    b_ref = list(bodies)
    n_ref = 10000
    dt_ref = total_time / n_ref
    for _ in range(n_ref):
        b_ref = rk4_step(b_ref, dt_ref, direct_gravity, G=1.0, softening=0.0)

    # Error in position of test particle (body index 1)
    err1 = b1[1].pos.distance_to(b_ref[1].pos)
    err2 = b2[1].pos.distance_to(b_ref[1].pos)

    # For 4th order global convergence: err(dt/2) / err(dt) ~ (1/2)^4 = 1/16
    ratio = err1 / max(err2, 1e-30)
    print(f"RK4 convergence: err1={err1:.6e}, err2={err2:.6e}, ratio={ratio:.1f} (expect ~16)")
    assert 8 < ratio < 32, f"Expected ~16x reduction, got {ratio:.1f}x"


def test_rk4_with_gravity():
    """RK4 with gravity produces plausible orbit."""
    bodies = [
        Body(1.0, Vec2(0, 0), Vec2(0, 0)),
        Body(1e-6, Vec2(1, 0), Vec2(0, 1)),
    ]
    for _ in range(100):
        bodies = rk4_step(bodies, 0.01, direct_gravity, G=1.0, softening=0.0)
    dist = bodies[0].pos.distance_to(bodies[1].pos)
    assert 0.5 < dist < 1.5
